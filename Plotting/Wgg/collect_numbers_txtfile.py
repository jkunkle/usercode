import re
import os
import pickle
from uncertainties import ufloat
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--baseDir', dest='baseDir', default=None, help='Path to final plots' )
parser.add_argument( '--bkgDir', dest='bkgDir', default=None, help='Path to final plots' )
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

    bkg_file_mu = 'cross_section_table_entries_muon.pickle'
    bkg_file_el = 'cross_section_table_entries_electron.pickle'

    ofile_bkg_mu = open( '%s/%s' %( options.bkgDir, bkg_file_mu), 'r')
    ofile_bkg_el = open( '%s/%s' %( options.bkgDir, bkg_file_el), 'r')

    data_bkg_mu = pickle.load( ofile_bkg_mu )
    data_bkg_el = pickle.load( ofile_bkg_el )

    ofile_bkg_mu.close()
    ofile_bkg_el.close()

    write_text_file( options.outputDir, data_mu,data_bkg_mu,sublPt=options.sublPt, prefix = 'results_MuonChannel_' )
    write_text_file( options.outputDir, data_el,data_bkg_el,sublPt=options.sublPt, prefix = 'results_ElectronChannel_' )
    #write_text_file_alberto( options.outputDir, data_mu, data_bkg_mu, sublPt=options.sublPt, channel = 'MuonChannel' )
    #write_text_file_alberto( options.outputDir, data_el, data_bkg_el, sublPt=options.sublPt, channel = 'ElectronChannel' )

def write_text_file( output_dir, data, data_bkg, sublPt=15, prefix = '' ) :

    if not os.path.isdir( output_dir ) :
        os.makedirs( output_dir ) 

    bin_info = get_binned_data( data )

    source_order = ['Data', 'Wgg', 'AllBkg']

    for source in source_order :

        fname = '%s%s.txt' %( prefix, source )
        ofile = open( '%s/%s' %( output_dir, fname ), 'w' )

        for bin, source_info in bin_info.iteritems() :
            
            if source != 'AllBkg' :
                sdata = source_info[source]

                val = sdata.n
                err = sdata.s

            else :

                bkg_bin = ( bin[1][0], bin[1][1], str(bin[0][0]), 'max')

                if bkg_bin not in data_bkg :
                    continue
                sdata = data_bkg[bkg_bin] 
                val = sdata.n
                err = sdata.s

                output_str = '%d-%d-%s%s %f %f' %( bin[0][0], sublPt, bin[1][0], bin[1][1], val, err )

                ofile.write( '%s\n' %( output_str) )

        ofile.close()

def write_text_file_alberto( output_dir, data, data_bkg, sublPt=15, channel = '' ) :

    if not os.path.isdir( output_dir ) :
        os.makedirs( output_dir ) 


    bin_info = get_binned_data( data )

        #        output_str = '%d-%d-%s%s %f %f' %( pt[0], sublPt, reg[0], reg[1], val.n, val.s )

        #        ofile.write( '%s\n' %( output_str) )

        #ofile.close()
    ofile = open( '%s/%s' %( output_dir, 'results.txt'), 'a' )
    print bin_info
    for bin, source in bin_info.iteritems() :
        print bin

        if bin[0][0] == 70  :
            val_data = source['Data'].n
            val_sig = source['Wgg'].n

            val_bkg = data_bkg[( bin[1][0], bin[1][1], str(bin[0][0]), 'max')] 

            cv_bkg = val_bkg.n
            err_bkg = val_bkg.s

            val_bkg_up = cv_bkg + err_bkg
            val_bkg_dn = cv_bkg - err_bkg

            output_str = '%s_%d-%d-%s%s %d %f %f %f %f' %( channel, bin[0][0], sublPt, bin[1][0], bin[1][1], val_data, val_sig, cv_bkg, val_bkg_up, val_bkg_dn )

            ofile.write( '%s\n' %( output_str ) )

def get_binned_data( input_data ) :

    bin_info = {}
    for source, sdata in input_data.iteritems() :

        for reg, ptdata in sdata.iteritems() :

            for pt, val in ptdata.iteritems() :

                bin = ( ( int(pt[0]), int(pt[1])), reg )
                bin_info.setdefault(bin, {})
                bin_info[bin][source] = val

    return bin_info


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

