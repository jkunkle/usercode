import math
import pickle
from argparse import ArgumentParser

from uncertainties import ufloat

parser = ArgumentParser()

parser.add_argument( '--baseDir', default=None, required=True, dest='baseDir', help='path to results' )

options = parser.parse_args()

acceptances = { 'electron' : {
                              ('15', '25')  : ufloat( 0.1505, 0.0091 ) , 
                              ('25', '40')  : ufloat( 0.1828, 0.0083 ) ,
                              ('40', '70')  : ufloat( 0.2237, 0.0091 ) ,
                              ('70', 'max') : ufloat( 0.2777, 0.0103 ) ,
                             },
                'muon'    : { 
                              ('15', '25')  : ufloat( 0.3065, 0.0149 ) , 
                              ('25', '40')  : ufloat( 0.3251, 0.0119 ) ,
                              ('40', '70')  : ufloat( 0.3398, 0.0117 ) ,
                              ('70', 'max') : ufloat( 0.3622, 0.0122 ) ,
                             },
}

def main() :

    file_electron = '%s/pt_leadph12_egg.pickle' %options.baseDir
    file_muon     = '%s/pt_leadph12_mgg.pickle' %options.baseDir

    results = {}

    ofile_electron = open( file_electron )
    results['electron'] = pickle.load( ofile_electron )
    ofile_electron.close()

    ofile_muon = open( file_muon )
    results['muon'] = pickle.load( ofile_muon )
    ofile_muon.close()

    pt_bins = ['15', '25', '40', '70', 'max']

    lumi = ufloat( 19.4, 19.4*0.011 )
    xs_data = {}
    for ch, res in results.iteritems() :

        print '***********************'
        print 'Channel %s' %ch
        print '***********************'

        all_xs = []

        xs_data[ch] = {}


        for idx, ptmin in enumerate( pt_bins[:-1] ) :

            ptmax = pt_bins[idx+1]

            acceptance = acceptances[ch][(ptmin,ptmax)]

            data = res['detail']['Data']['bins'][str(idx+4)]['val']

            bkg = ufloat( 0.0, 0.0 )
            sig = ufloat( 0.0, 0.0 )

            bkg = bkg + res['detail']['Zgg']['bins'][str(idx+4)]['val']
            bkg = bkg + res['detail']['JetFake']['bins'][str(idx+4)]['val']
            bkg = bkg + res['detail']['OtherDiPhoton']['bins'][str(idx+4)]['val']

            if ch=='electron' :
                bkg = bkg + res['detail']['EleFake']['bins'][str(idx+4)]['val']

            sig = sig + res['detail']['Wgg']['bins'][str(idx+4)]['val']
            sig = ufloat( sig.n, math.sqrt( sig.n ) )


            data_minus_bkg = data - bkg


            cross_section = ( data_minus_bkg ) / ( acceptance * lumi )
            cross_section_exp = ( sig + ufloat( 0.0, bkg.s) ) / ( acceptance * lumi )

            xs_data[ch][( ptmin, ptmax)] = {'acceptance' : acceptance, 'bkg' : bkg, 'sig' : sig, 'data' : data, 'cross_section' : cross_section, 'cross_section_exp' : cross_section_exp }

            all_xs.append(cross_section)

            print 'Pt bin : %s - %s' %( ptmin, ptmax )
            print 'Data = %s, Background = %s, Diff = %s' %(data, bkg, data_minus_bkg)
            print 'Signal = %s' %sig
            print 'acceptance = %s ' %acceptance
            print 'Expected cross section = %s fb' %cross_section_exp
            print 'Cross section = %s fb' %cross_section


        sum_xs = reduce( lambda x, y : x + y, all_xs )

        print 'Summed cross section = %s fb' %sum_xs


    rev_ptbins = list( pt_bins )
    rev_ptbins.reverse()
    for ch in results.keys() :
        cross_section = ufloat( 0.0, 0.0 )
        cross_section_exp = ufloat( 0.0, 0.0 )

        print 'Reverse cumulative sum, channel = %s' %ch
        
        for idx, ptmax in enumerate( rev_ptbins[:-1] ) :
            ptmin = rev_ptbins[idx+1]

            cross_section = cross_section + xs_data[ch][( ptmin, ptmax )]['cross_section']
            cross_section_exp = cross_section_exp + xs_data[ch][( ptmin, ptmax )]['cross_section_exp']

            print 'Pt bin : %s - %s' %( ptmin, ptmax )
            print 'Expected cross section = %s' %cross_section_exp
            print 'Cross section = %s' %cross_section


        
    ofile = open( '%s/cross_section_results.pickle' %(options.baseDir ), 'w' )

    pickle.dump(xs_data, ofile )

    ofile.close()






main()
