from uncertainties import ufloat
import pickle
import math

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--baseDir', dest='baseDir', default=None,  help = 'plot directory' )
parser.add_argument( '--nBins', dest='nBins', default=0, type=int, help = 'plot directory' )

options = parser.parse_args()

def main() :

    ofile_mu  = open( '%s/pt_leadph12_muhighmt.pickle' %options.baseDir )
    ofile_ele = open( '%s/pt_leadph12_elfullhighmt.pickle' %options.baseDir )

    res_ele = pickle.load( ofile_ele )
    res_mu  = pickle.load( ofile_mu  )

    ofile_mu.close()
    ofile_ele.close()

    ptbins = res_ele['detail']['Wgg']['bins'].keys()
    ptbins.sort()
    ptbins.reverse()

    print ptbins

    total_ele_bkg = ufloat( 0.0, 0.0 )
    total_ele_sig = ufloat( 0.0, 0.0 )
    total_mu_bkg  = ufloat( 0.0, 0.0 )
    total_mu_sig  = ufloat( 0.0, 0.0 )

    for idx, bin in enumerate( ptbins ) :

        if idx >= options.nBins:
            break

        print 'include bin ', bin

        for samp, res in res_mu['detail'].iteritems() :

            print samp

            if samp == 'err_band' :
                continue
            if samp == 'Data' :
                continue
            if samp == 'AllBkg' :
                continue

            if samp == 'Wgg'  :
                total_mu_sig += res['bins'][bin]['val']
            else :
                print 'Add %s to bkg' %samp
                total_mu_bkg += res['bins'][bin]['val']

        for samp, res in res_ele['detail'].iteritems() :

            if samp == 'err_band' :
                continue
            if samp == 'Data' :
                continue
            if samp == 'AllBkg' :
                continue

            if samp == 'Wgg'  :
                total_ele_sig += res['bins'][bin]['val']
            else :
                total_ele_bkg += res['bins'][bin]['val']

    
    #print 'Muon Sig = %s, bkg  = %s, s/sqrt(b) = %f ' %( total_mu_sig, total_mu_bkg, total_mu_sig.n/ math.sqrt(total_mu_bkg.n)  )
    #print 'Electron Sig = %s, bkg  = %s, s/sqrt(b) = %f  ' %( total_ele_sig, total_ele_bkg, total_ele_sig.n/math.sqrt(total_ele_bkg.n)  )
    #print 'Muon Sig = %s, bkg  = %s, s/sqrt(b) = %f ' %( total_mu_sig, total_mu_bkg, total_mu_sig.n/ ( total_mu_sig.n+ total_mu_bkg.s  ) )
    #print 'Electron Sig = %s, bkg  = %s, s/sqrt(b) = %f  ' %( total_ele_sig, total_ele_bkg, total_ele_sig.n/(total_ele_sig.n+ total_ele_bkg.s  ) )
    print 'Muon Sig = %s, bkg  = %s, s/sqrt(b) = %f ' %( total_mu_sig, total_mu_bkg, total_mu_sig.n/ ( total_mu_bkg.s  ) )
    print 'Electron Sig = %s, bkg  = %s, s/sqrt(b) = %f  ' %( total_ele_sig, total_ele_bkg, total_ele_sig.n/(total_ele_bkg.s  ) )




main()

