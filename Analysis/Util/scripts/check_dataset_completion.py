
from argparse import ArgumentParser

import os
import eos_utilities as eosutil
import ROOT

# disable file recovery
ROOT.gEnv.SetValue('TFile.Recover', 'OFF' )
#ROOT.gEnv.SaveLevel( ROOT.kEnvGlobal )



def main() :

    parser = ArgumentParser()
    
    parser.add_argument('--originalDS', dest='originalDS', default=None, required=True,help='Path to original dataset')
    parser.add_argument('--filteredDS', dest='filteredDS', default=None, required=True,help='Path to filtered dataset')
    parser.add_argument('--treeNameOrig',   dest='treeNameOrig',   default=None, required=False, help='Name of tree in original sample.  Use --treeNameOrig to read events from the tree or --histNameOrig to read from the histogram')
    parser.add_argument('--treeNameFilt',   dest='treeNameFilt',   default=None, required=False, help='Name of tree in filtered sample.  Use --treeNameFilt to read events from the tree or --histNameFilt to read from the histogram')
    parser.add_argument('--histNameOrig',   dest='histNameOrig',   default=None, required=False, help='Name of hist in original sample.  Use --treeNameOrig to read events from the tree or --histNameOrig to read from the histogram')
    parser.add_argument('--histNameFilt',   dest='histNameFilt',   default=None, required=False, help='Name of hist in filtered sample.  Use --treeNameFilt to read events from the tree or --histNameFilt to read from the histogram')
    parser.add_argument('--fileKeyOrig', dest='fileKeyOrig', default=None, help='key to match orginal files' )
    parser.add_argument('--fileKeyFilt', dest='fileKeyFilt', default=None, help='key to match filtered files' )
    
    options = parser.parse_args()

    orig_nevt_tree, orig_nevt_hist, filt_nevt_tree, filt_nevt_hist = check_dataset_completion( options.originalDS, options.filteredDS, options.treeNameOrig, options.treeNameFilt, options.histNameOrig, options.histNameFilt, options.fileKeyOrig, options.fileKeyFilt )

    orig_nevt = orig_nevt_tree
    if not orig_nevt :
        orig_nevt = orig_nevt_hist

    filt_nevt = filt_nevt_tree
    if not filt_nevt :
        filt_nevt = filt_nevt_hist


    print '%s : Orignal = %d events, filtered = %d events.  Difference = %d' %( options.filteredDS.split('/')[-1], orig_nevt, filt_nevt, orig_nevt-filt_nevt)

def check_dataset_completion( originalDS, filteredDS, treeNameOrig=None, treeNameFilt=None, histNameOrig=None, histNameFilt=None, fileKeyOrig=None, fileKeyFilt=None ) :

    assert treeNameOrig is not None or histNameOrig is not None, 'Must provide a histogram or tree name for original samples'
    assert treeNameFilt is not None or histNameFilt is not None, 'Must provide a histogram or tree name for filtered samples'

    #assert not (treeNameOrig is not None and histNameOrig is not None), 'Must provide a histogram or tree name for original samples, not both'
    #assert not (treeNameFilt is not None and histNameFilt is not None), 'Must provide a histogram or tree name for filtered samples, not both'

    orig_nevt_tree = 0
    orig_nevt_hist = 0
    filt_nevt_tree = 0
    filt_nevt_hist = 0

    if originalDS.count( '/eos/' ) :
        for top, dirs, files, sizes in eosutil.walk_eos( originalDS ) :
            for file in files :

                if fileKeyOrig is not None and not file.count(fileKeyOrig) : continue

                ofile = ROOT.TFile.Open( 'root://eoscms/' + top+'/'+file )
                if treeNameOrig is not None :
                    try :
                        otree = ofile.Get(treeNameOrig)
                    except ReferenceError :
                        print 'Could not access file'
                        continue

                    try :
                        orig_nevt_tree += otree.GetEntries()
                    except AttributeError :
                        print 'Could not access hist'
                        continue

                if histNameOrig is not None :
                    try :
                        ohist = ofile.Get(histNameOrig)
                    except ReferenceError :
                        print 'Could not access file'
                        continue

                    try  :
                        orig_nevt_hist += ohist.GetBinContent(1)
                    except AttributeError :
                        print 'Could not access hist'
                        continue
    else :
        for top, dirs, files in os.walk( originalDS ) :
            for file in files :

                if fileKeyOrig is not None and not file.count(fileKeyOrig) : continue

                ofile = ROOT.TFile.Open( top+'/'+file )
                if treeNameOrig is not None :
                    try :
                        otree = ofile.Get(treeNameOrig)
                        orig_nevt_tree += otree.GetEntries()
                    except ReferenceError :
                        print 'Could not access file'

                if histNameOrig is not None :
                    try :
                        ohist = ofile.Get(histNameOrig)
                        orig_nevt_hist += ohist.GetBinContent(1)
                    except ReferenceError :
                        print 'Could not access file'



    if not orig_nevt_tree and not orig_nevt_hist  :
        print 'Did not get any original events.  Check the path'
        return orig_nevt_tree, orig_nevt_hist, filt_nevt_tree, filt_nevt_hist
        

    if filteredDS.count( '/eos/' ) :
        for top, dirs, files, sizes in eosutil.walk_eos( filteredDS ) :
            for file in files :

                if fileKeyFilt is not None and not file.count(fileKeyFilt) : continue

                ofile = ROOT.TFile.Open( 'root://eoscms/' + top+'/'+file )
                if ofile == None :
                    continue
                if  ofile.IsZombie() :
                    continue
                if ofile.TestBit(ROOT.TFile.kRecovered) :
                    print 'File was recovered, and data is probably not available'
                    continue
                if treeNameFilt is not None :
                    try :
                        otree = ofile.Get(treeNameFilt)
                        filt_nevt_tree += otree.GetEntries()
                    except ReferenceError :
                        print 'Could not access file'

                if histNameFilt is not None :
                    try :
                        ohist = ofile.Get(histNameFilt)
                    except ReferenceError :
                        print 'Could not access file'
                        continue

                    try  :
                        filt_nevt_hist += ohist.GetBinContent(1)
                    except AttributeError :
                        print 'Could not access hist'
                        continue


    else :
        for top, dirs, files in os.walk( filteredDS ) :
            for file in files :

                if fileKeyFilt is not None and not file.count(fileKeyFilt) : continue

                ofile = ROOT.TFile.Open( top+'/'+file )
                if ofile == None :
                    continue
                if ofile.IsZombie() :
                    continue
                if ofile.TestBit(ROOT.TFile.kRecovered) :
                    print 'File was recovered, and data is probably not available'
                    continue
                if treeNameFilt is not None :
                    try :
                        otree = ofile.Get(treeNameFilt)
                        filt_nevt_tree += otree.GetEntries()
                    except ReferenceError :
                        print 'Could not access file'

                if histNameFilt is not None :
                    try :
                        ohist = ofile.Get(histNameFilt)
                    except ReferenceError :
                        print 'Could not access file'
                    try :
                        filt_nevt_hist += ohist.GetBinContent(1)
                    except AttributeError :
                        print 'Could not get hist from file %s' %(top+'/'+file)




    return orig_nevt_tree, orig_nevt_hist, filt_nevt_tree, filt_nevt_hist



if __name__ == '__main__' :
    main()

