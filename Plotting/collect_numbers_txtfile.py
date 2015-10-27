import re
import os
import pickle
from uncertainties import ufloat
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--baseDir', dest='baseDir', default=None, help='Path to final plots' )
parser.add_argument( '--outputDir', dest='outputDir', default=None, help='Path to output dir' )
parser.add_argument( '--sublPt', dest='sublPt', type=int, default=-1, help='subleadpt' )

options = parser.parse_args()


def main() :

    if options.sublPt < 0 :
        print 'Must provide a sublead pT'
        return

    file_key_mu = 'pt_leadph12_muhighmt_(\w{2,2})-(\w{2,2}).*?\.pickle'
    file_key_el = 'pt_leadph12_elfullhighmt_(\w{2,2})-(\w{2,2}).*?\.pickle'

    data_files_mu = get_data_files_by_region( options.baseDir, file_key_mu )
    data_files_el = get_data_files_by_region( options.baseDir, file_key_el )

    data_mu = get_data_from_pickle( data_files_mu )
    data_el = get_data_from_pickle( data_files_el )

    write_text_file( options.outputDir, data_mu,sublPt=options.sublPt, prefix = 'results_MuonChannel_' )
    write_text_file( options.outputDir, data_el,sublPt=options.sublPt, prefix = 'results_ElectronChannel_' )

def write_text_file( output_dir, data, sublPt=15, prefix = '' ) :

    if not os.path.isdir( output_dir ) :
        os.makedirs( output_dir ) 

    for source, sdata in data.iteritems() :

        fname = '%s%s.txt' %( prefix, source )

        ofile = open( '%s/%s' %( output_dir, fname ), 'w' )

        for reg, ptdata in sdata.iteritems() :

            for pt, val in ptdata.iteritems() :

                output_str = '%d-%d-%s%s %f %f' %( pt[0], sublPt, reg[0], reg[1], val.n, val.s )

                ofile.write( '%s\n' %( output_str) )

        ofile.close()


def get_data_from_pickle( files_map ) :

    selected_entries = ['Wgg', 'Data', 'AllBkg']

    collected_data = {}

    for ent in selected_entries :
        collected_data[ent] = {}

        for reg, dfile in files_map.iteritems() :
            collected_data[ent][reg] = {}

            ofile = open( dfile )

            data = pickle.load( ofile )

            # find pt bins
            pt_bins = []
            for bins in data['detail'][ent]['bins'].values() :
                pt_bin =  ( bins['min'], bins['max'] ) 
                collected_data[ent][reg][pt_bin] = bins['val']

    return collected_data

def get_data_files_by_region(base_dir, file_key ) :

    found_files = {}

    for dfile in os.listdir( base_dir ) :

        print dfile

        res = re.match(  file_key, dfile  )
        
        if res is not None :

            region = ( res.group(1), res.group(2) )

            found_files[region] = '%s/%s' %(base_dir,dfile)

    return found_files








main()

