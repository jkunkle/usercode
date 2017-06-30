import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import os
import uuid
import time
import math
import re
import pickle

from SampleManager import SampleManager
from argparse import ArgumentParser
parser = ArgumentParser()

parser = ArgumentParser()
parser.add_argument('--baseDir',      default=None,           dest='baseDir',         required=True, help='Path to muon base directory')
parser.add_argument('--samplesConf',  default=None,           dest='samplesConf',     required=True, help='Sample configuration' )

options = parser.parse_args()



_TREENAME = 'tupel/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36200
_BASEPATH = '/home/jkunkle/usercode/Plotting/LimitSetting/'



def main() :

    sampMan = SampleManager( options.baseDir, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    if options.samplesConf is not None :

        sampMan.ReadSamples( options.samplesConf )
    else :
        print 'Must provide a sample configuration.  Exiting'
        return


    var = 'mt_res'
    selection = 'mu_n==1 && ph_n==1'
    binning = ( 100, 0, 5000 )
    bkg_samp = 'MCBackground'
    sampMan.create_hist( bkg_samp, var,  selection, binning )

    bkg_hist = sampMan.get_samples( name=bkg_samp)[0].hist

    sig_normalizations = {}
    for samp in sampMan.get_samples( )  :
        if samp.name.count ( 'ResonanceMass' ) and samp.name.count( 'width0p01' ) :

            sampMan.create_hist( samp, var,  selection, binning )

            samp_bins = []

            for ibin in range( 0, samp.hist.GetNbinsX()  ) :

                samp_bins.append( (samp.hist.GetBinContent( ibin+1 ), ibin+1 ) )

            samp_bins.sort()
            print samp_bins

            peak_sum = samp_bins[-1][0] 
            bkg_sum = bkg_hist.GetBinContent( samp_bins[-1][1] ) 
            print 'Samp = %s, sig = %f, bkg = %f' %(samp.name, peak_sum, bkg_sum )


            sig_normalizations[samp.name] = float( bkg_sum )/peak_sum

    print sig_normalizations



main()


