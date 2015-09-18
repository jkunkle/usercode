import pickle
import math
import os
import ROOT

from uncertainties import ufloat

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--origPath', dest='origPath', default=None, help='Path to set of original files' )
parser.add_argument( '--newPath', dest='newPath', default=None, help='Path to set of new files' )
parser.add_argument( '--fileKey', dest='fileKey', default=None, help='key to match files' )
parser.add_argument( '--dictKey', dest='dictKey', default=None, help='key to match dictionary entries' )
    
options = parser.parse_args()

def main() :

    options.origPath = options.origPath.rstrip('/')
    options.newPath = options.newPath.rstrip('/')
        
    orig_files = []
    for top, dirs, files in os.walk( options.origPath ) :
        for f in files :
            if f.count( '.pickle' ) :
                if options.fileKey is not None :
                    if f.count( options.fileKey ) :
                        orig_files.append( top + '/' + f )
                else :
                    orig_files.append( top + '/' + f )

    new_files = []
    for top, dirs, files in os.walk( options.newPath ) :
        for f in files :
            if f.count( '.pickle' ) :
                if options.fileKey is not None :
                    if f.count( options.fileKey ) :
                        new_files.append( top + '/' + f )
                else :
                    new_files.append( top + '/' + f )

    for ofile in orig_files :
        for nfile in new_files :

            ocomp = ofile[len(options.origPath):]
            ncomp = nfile[len(options.newPath):]
            if ocomp==ncomp:
                print ofile
                compare_files( ofile, nfile, dictKey=options.dictKey )




    
def compare_files( ofile, nfile, dictKey=None ) :

    oofile = open( ofile )
    odic = pickle.load( oofile )
    oofile.close()

    onfile = open( nfile )
    ndic = pickle.load( onfile )
    onfile.close()

    for key, val in odic.iteritems() :

        if dictKey is not None :
            if not key.count( dictKey ) :
                continue
        try :
            diff = val - ndic[key]
            if math.fabs( diff ) > 0.01 :
                print 'key = %s, diff = %s, orig = %s, new = %s' %( key, diff, val, ndic[key] )
        except :
            continue








main()
