
import pickle
from argparse import ArgumentParser

from uncertainties import ufloat

parser = ArgumentParser()

parser.add_argument( '--baseDir', default=None, required=True, dest='baseDir', help='path to results' )

options = parser.parse_args()

acceptances = { 'electron' : {
                              ('15', '25') : 0.1684, 
                              ('25', '40') : 0.1926,
                              ('40', '70') : 0.2474,
                              ('70', 'max') : 0.3095,
                             },
                'muon'    : {
                              ('15', '25') : 0.3494, 
                              ('25', '40') : 0.3647,
                              ('40', '70') : 0.3947,
                              ('70', 'max') : 0.4233,
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
    for ch, res in results.iteritems() :

        print '***********************'
        print 'Channel %s' %ch
        print '***********************'

        all_xs = []

        for idx, ptmin in enumerate( pt_bins[:-1] ) :

            ptmax = pt_bins[idx+1]

            acceptance = ufloat( acceptances[ch][(ptmin,ptmax)], 0.0 )

            data = res['detail']['Data']['bins'][str(idx+4)]['val']

            bkg = ufloat( 0.0, 0.0 )

            bkg = bkg + res['detail']['ZggFSR']['bins'][str(idx+4)]['val']
            bkg = bkg + res['detail']['JetFake']['bins'][str(idx+4)]['val']

            if ch=='electron' :
                bkg = bkg + res['detail']['EleFake']['bins'][str(idx+4)]['val']

            data_minus_bkg = data - bkg


            cross_section = ( data_minus_bkg ) / ( acceptance * lumi )

            all_xs.append(cross_section)

            print 'Pt big : %s - %s' %( ptmin, ptmax )
            print 'Data = %s, Background = %s, Diff = %s' %(data, bkg, data_minus_bkg)
            print 'acceptance = %s ' %acceptance
            print 'Cross section = %s fb' %cross_section


        sum_xs = reduce( lambda x, y : x + y, all_xs )

        print 'Summed cross section = %s fb' %sum_xs




main()
