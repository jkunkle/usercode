from argparse import ArgumentParser

import pickle

parser = ArgumentParser()

parser.add_argument( '--baseDir', default=None, dest='baseDir', help = 'path to directory with cross section pickle files' )
parser.add_argument( '--outputFile', default=None, dest='outputFile', help = 'name of output file' )


options = parser.parse_args()


def main() :

    ofile = open( options.cxFile, 'r' )

    xs_info = pickle.load( ofile )

    ofile.close()

    channels = ['muon', 'electron']
    pt_bins = [('70', 'max') ]

    all_sources = [
                   'statDataSB',        
                   'statDataSR',        
                   'crossCorr',  
                   'systBkg',    
                   'systTemp',   
                   'statTemp1D', 
                   'statTempFF', 
                   'fakefake', 
                   'EleFakeFF',         
                   'ZggStat',           
                   'ZggSyst',           
                   'OtherDiPhotonStat', 
                   'OtherDiPhotonSyst', 
                   #'lumi',              
    ]
    el_comb_syst = {
                                            'crossCorr' : True,
                                            'systBkg' : True,
                                            'fakefake' : False,
                                            'systTemp' : False,
                                            'statTemp1D' : False,
                                            'statTempFF' : False,
                                            'statDataSB' : False,
                                            'statDataSR' : False,
                                            'EleFakeFF' : False  }


    basic_sources = ['ZggStat', 'ZggSyst', 'OtherDiPhotonStat', 'OtherDiPhotonSyst']

    regions = [('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB') ]

    for ch in channels :

        for sidx,syst in enumerate(all_sources) :
            if ch=='muon' and syst=='EleFakeFF' :
                continue

                totals_all.setdefault( rbin, ufloat(val.n,0) )
                totals_all[rbin] = totals_all[rbin] + ufloat( 0.0, val.s )




main()
