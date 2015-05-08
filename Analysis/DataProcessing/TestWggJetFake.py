import pickle
import ROOT
from uncertainties import ufloat
from uncertainties import unumpy
import math

from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument('--file', dest='file', default=None, required=True, help='Path to input file' )
parser.add_argument('--scanFLLead', dest='scanFLLead', default=False, action='store_true', help='Path to input file' )
parser.add_argument('--scanFLSubl', dest='scanFLSubl', default=False, action='store_true', help='Path to input file' )
parser.add_argument('--scanRLLead', dest='scanRLLead', default=False, action='store_true', help='Path to input file' )
parser.add_argument('--scanCorrTT', dest='scanCorrTT', default=False, action='store_true', help='scan correlation on TT relative to LL' )
parser.add_argument('--scanCorrTLLT', dest='scanCorrTLLT', default=False, action='store_true', help='scan correlation on TL and LT' )
parser.add_argument('--scanCorrTTLL', dest='scanCorrTTLL', default=False, action='store_true', help='scan correlation on TL and LT' )
parser.add_argument('--test', dest='test', default=False, action='store_true', help='test mode' )

options = parser.parse_args()

def main() :

    hist_scan = ROOT.TGraph( 100 )
    hist_scan.SetName( 'hist_scan' )

    ofile = open( options.file, 'r' )

    info = pickle.load( ofile )

    eff_1d = info['eff_1d']

    eff_R_L_lead = eff_1d['eff_R_L_lead']
    eff_F_L_lead = eff_1d['eff_F_L_lead']

    eff_R_L_subl = eff_1d['eff_R_L_subl']
    eff_F_L_subl = eff_1d['eff_F_L_subl']

    data_TT = info['Ndata_TT']
    data_TL = info['Ndata_TL']
    data_LT = info['Ndata_LT']
    data_LL = info['Ndata_LL']

    data = [data_TT, data_TL, data_LT, data_LL]

    print 'Data TT = ', data_TT
    print 'Data TL = ', data_TL
    print 'Data LT = ', data_LT
    print 'Data LL = ', data_LL
    
    scan_max_lim = 0.9
    scan_min_lim = 0.1

    eff_scan_F_L_lead = []
    eff_scan_F_L_subl = []
    eff_scan_R_L_lead = []
    eff_scan_R_L_subl = []

    if options.scanFLLead :
        scan_max = eff_F_L_lead + 0.3
        scan_min = eff_F_L_lead - 0.3

        if scan_max > scan_max_lim :
            scan_max = scan_max_lim
            scan_min = scan_min - ( scan_max - scan_max_lim )
        if scan_min < scan_min_lim :
            scan_min = scan_min_lim
            scan_max = scan_max + ( scan_min_lim - scan_min ) 

        # make 100 points between min and max
        scan_step = ( scan_max - scan_min ) / 100.
        for i in range( 0, 100 ) :
            eff_scan_F_L_lead.append( scan_min+i*scan_step )
            eff_scan_F_L_subl.append( eff_F_L_subl )
            #eff_scan_F_L_subl.append( scan_min+i*scan_step )
            
            eff_scan_R_L_lead.append( eff_R_L_lead )
            eff_scan_R_L_subl.append( eff_R_L_subl )


        scan_result = scan_fit_1d( eff_scan_R_L_lead, eff_scan_R_L_subl, eff_scan_F_L_lead, eff_scan_F_L_subl, data )
        scan_nominal = scan_fit_1d( [eff_R_L_lead], [eff_R_L_subl], [eff_F_L_lead], [eff_F_L_subl], data )

        for idx, result in enumerate( scan_result ) :
            input = eff_scan_F_L_lead[idx]

            hist_scan.SetPoint( idx, input.n, result['sum'].n )

        marker = ROOT.TMarker(eff_F_L_lead.n,scan_nominal[0]['sum'].n, 20 )

        hist_scan.Draw('AL')
        marker.Draw()
        raw_input("cont")


    if options.scanFLSubl :
        scan_max = eff_F_L_subl + 0.3
        scan_min = eff_F_L_subl - 0.3

        if scan_max > scan_max_lim :
            scan_max = scan_max_lim
            scan_min = scan_min - ( scan_max - scan_max_lim )
        if scan_min < scan_min_lim :
            scan_min = scan_min_lim
            scan_max = scan_max + ( scan_min_lim - scan_min ) 

        # make 100 points between min and max
        scan_step = ( scan_max - scan_min ) / 100.
        for i in range( 0, 100 ) :
            eff_scan_F_L_subl.append( scan_min+i*scan_step )
            eff_scan_F_L_lead.append( eff_F_L_lead )

            eff_scan_R_L_lead.append( eff_R_L_lead )
            eff_scan_R_L_subl.append( eff_R_L_subl )

        scan_result = scan_fit_1d( eff_scan_R_L_lead, eff_scan_R_L_subl, eff_scan_F_L_lead, eff_scan_F_L_subl, data )
        scan_nominal = scan_fit_1d( [eff_R_L_lead], [eff_R_L_subl], [eff_F_L_lead], [eff_F_L_subl], data )

        for idx, result in enumerate( scan_result ) :
            input = eff_scan_F_L_subl[idx]

            hist_scan.SetPoint( idx, input.n, result['sum'].n )

        marker = ROOT.TMarker(eff_F_L_subl.n,scan_nominal[0]['sum'].n, 20 )

        hist_scan.Draw('AL')
        marker.Draw()
        raw_input("cont")

    if options.scanRLLead :
        scan_max_lim = 0.99
        scan_min_lim = 0.01

        scan_max = eff_R_L_lead + 0.3
        scan_min = eff_R_L_lead - 0.3

        if scan_max > scan_max_lim :
            scan_max = scan_max_lim
            scan_min = scan_min - ( scan_max - scan_max_lim )
        if scan_min < scan_min_lim :
            scan_min = scan_min_lim
            scan_max = scan_max + ( scan_min_lim - scan_min ) 

        # make 100 points between min and max
        scan_step = ( scan_max - scan_min ) / 100.
        for i in range( 0, 100 ) :
            eff_scan_R_L_lead.append( scan_min+i*scan_step )
            eff_scan_R_L_subl.append( eff_R_L_subl )
            #eff_scan_F_L_subl.append( scan_min+i*scan_step )
            
            eff_scan_F_L_lead.append( eff_F_L_lead )
            eff_scan_F_L_subl.append( eff_F_L_subl )


        scan_result = scan_fit_1d( eff_scan_R_L_lead, eff_scan_R_L_subl, eff_scan_F_L_lead, eff_scan_F_L_subl, data )
        scan_nominal = scan_fit_1d( [eff_R_L_lead], [eff_R_L_subl], [eff_F_L_lead], [eff_F_L_subl], data )

        for idx, result in enumerate( scan_result ) :
            input = eff_scan_R_L_lead[idx]

            hist_scan.SetPoint( idx, input.n, result['sum'].n )

        marker = ROOT.TMarker(eff_R_L_lead.n,scan_nominal[0]['sum'].n, 20 )
        

        hist_scan.Draw('AL')
        marker.Draw()
        raw_input("cont")

    if options.scanCorrTT :

        scan_matrices = []

        eff_2d_orig = generate_2d_efficiencies( eff_R_L_lead, eff_R_L_subl, eff_F_L_lead, eff_F_L_subl )

        scan_min = -1
        scan_max = 1
        scan_step = (scan_max - scan_min ) / 100.

        for i in range( 0, 100 ) :
            eff_2d = dict( eff_2d_orig )
            eff_2d['FF_TT']  = eff_2d['FF_TT']* ( 1+ (scan_min+(scan_step*i)) )
            eff_2d['FF_LL'] = 1 - eff_2d['FF_TT'] - eff_2d['FF_TL'] - eff_2d['FF_LT']

            print eff_2d['FF_TT']
            print eff_2d['FF_LL']


            scan_matrices.append( eff_2d )

        scan_result = scan_fit_2d( scan_matrices, data )

        for idx, result in enumerate( scan_result ) :
            input = scan_min+(scan_step*idx)

            hist_scan.SetPoint( idx, input, result['sum'].n )

        hist_scan.Draw('AL')
        raw_input("cont")

    if options.scanCorrTLLT :

        scan_matrices = []

        eff_2d_orig = generate_2d_efficiencies( eff_R_L_lead, eff_R_L_subl, eff_F_L_lead, eff_F_L_subl )

        scan_min = -1
        scan_max = 1
        scan_step = (scan_max - scan_min ) / 100.

        for i in range( 0, 100 ) :
            eff_2d = dict( eff_2d_orig )
            eff_2d['FF_TL']  = eff_2d['FF_TL']* ( 1+ (scan_min+(scan_step*i)) )
            eff_2d['FF_LT']  = eff_2d['FF_LT']* ( 1+ (scan_min+(scan_step*i)) )

            target = 1 - eff_2d['FF_TL'] - eff_2d['FF_LT']

            TT_LL_ratio = eff_2d['FF_TT']/eff_2d['FF_LL']

            eff_2d['FF_LL'] = target / ( 1 + TT_LL_ratio )

            eff_2d['FF_TT'] = 1 - eff_2d['FF_LL'] - eff_2d['FF_TL'] - eff_2d['FF_LT']


            scan_matrices.append( eff_2d )

        scan_result = scan_fit_2d( scan_matrices, data )

        for idx, result in enumerate( scan_result ) :
            input = scan_min+(scan_step*idx)

            hist_scan.SetPoint( idx, input, result['sum'].n )

        hist_scan.Draw('AL')
        raw_input("cont")

    if options.scanCorrTTLL :

        scan_matrices = []

        eff_2d_orig = generate_2d_efficiencies( eff_R_L_lead, eff_R_L_subl, eff_F_L_lead, eff_F_L_subl )

        scan_min = -1
        scan_max = 1
        scan_step = (scan_max - scan_min ) / 100.

        for i in range( 0, 100 ) :
            eff_2d = dict( eff_2d_orig )
            eff_2d['FF_TT']  = eff_2d['FF_TT']* ( 1+ (scan_min+(scan_step*i)) )
            eff_2d['FF_LL']  = eff_2d['FF_LL']* ( 1+ (scan_min+(scan_step*i)) )

            target = 1 - eff_2d['FF_TT'] - eff_2d['FF_LL']

            TL_LT_ratio = eff_2d['FF_TL']/eff_2d['FF_LT']

            eff_2d['FF_LT'] = target / ( 1 + TL_LT_ratio )

            eff_2d['FF_TL'] = 1 - eff_2d['FF_LL'] - eff_2d['FF_LT'] - eff_2d['FF_TT']


            scan_matrices.append( eff_2d )

        scan_result = scan_fit_2d( scan_matrices, data )

        for idx, result in enumerate( scan_result ) :
            input = scan_min+(scan_step*idx)

            hist_scan.SetPoint( idx, input, result['sum'].n )

        hist_scan.Draw('AL')
        raw_input("cont")

    if options.test :

        eff_2d_orig = generate_2d_efficiencies( eff_R_L_lead, eff_R_L_subl, eff_F_L_lead, eff_F_L_subl )
    
        eff_2d = dict( eff_2d_orig )

        print 'FF_TT orig = ', eff_2d['FF_TT']
        print 'FF_TL orig = ', eff_2d['FF_TL']
        print 'FF_LT orig = ', eff_2d['FF_LT']
        print 'FF_LL orig = ', eff_2d['FF_LL']

        eff_2d['FF_TT'] = ufloat( 0.029,0.016  )
        eff_2d['FF_TL'] = ufloat( 0.067,0.025 )
        eff_2d['FF_LT'] = ufloat( 0.144,0.034 )
        eff_2d['FF_LL'] = ufloat( 0.76,0.04 )

        ## ChHadIso 15-25
        #eff_2d['FF_TT'] = ufloat( 0.068, 0.009)
        #eff_2d['FF_TL'] = ufloat( 0.063, 0.008)
        #eff_2d['FF_LT'] = ufloat( 0.080, 0.010)
        #eff_2d['FF_LL'] = ufloat( 0.789, 0.014)
        
        ## ChHadIso 25-40
        #eff_2d['FF_TT'] = ufloat( 0.032, 0.007)
        #eff_2d['FF_TL'] = ufloat( 0.049, 0.008)
        #eff_2d['FF_LT'] = ufloat( 0.051, 0.008)
        #eff_2d['FF_LL'] = ufloat( 0.867, 0.012)

        ## ChHadIso 40-70
        #eff_2d['FF_TT'] = ufloat( 0.018, 0.006 )
        #eff_2d['FF_TL'] = ufloat( 0.051, 0.010 )
        #eff_2d['FF_LT'] = ufloat( 0.069, 0.012 )
        #eff_2d['FF_LL'] = ufloat( 0.862 , 0.016  )

        # ChHadIso >70
        #eff_2d['FF_TT'] = ufloat( 0.003, 0.003)
        #eff_2d['FF_TL'] = ufloat( 0.031, 0.010)
        #eff_2d['FF_LT'] = ufloat( 0.042, 0.012)
        #eff_2d['FF_LL'] = ufloat( 0.924, 0.016)

        ## EMIso 15-25
        #eff_2d['FF_TT'] = ufloat( 0.035, 0.009)
        #eff_2d['FF_TL'] = ufloat( 0.150, 0.017)
        #eff_2d['FF_LT'] = ufloat( 0.148, 0.017)
        #eff_2d['FF_LL'] = ufloat( 0.667, 0.022)
        
        ## EMIso 25-40
        #eff_2d['FF_TT'] = ufloat( 0.037, 0.009)
        #eff_2d['FF_TL'] = ufloat( 0.140, 0.017)
        #eff_2d['FF_LT'] = ufloat( 0.158, 0.017)
        #eff_2d['FF_LL'] = ufloat( 0.666, 0.023)

        ## EMIso 40-70
        #eff_2d['FF_TT'] = ufloat( 0.021, 0.009)
        #eff_2d['FF_TL'] = ufloat( 0.120, 0.021)
        #eff_2d['FF_LT'] = ufloat( 0.158, 0.017)
        #eff_2d['FF_LL'] = ufloat( 0.701, 0.030)

        ## EMIso >70
        #eff_2d['FF_TT'] = ufloat( 0.037, 0.018)
        #eff_2d['FF_TL'] = ufloat( 0.093, 0.028)
        #eff_2d['FF_LT'] = ufloat( 0.168, 0.036)
        #eff_2d['FF_LL'] = ufloat( 0.701, 0.044)


        ## sigmaIEIE 15-25
        #eff_2d['FF_TT'] = ufloat( 0.141, 0.016)
        #eff_2d['FF_TL'] = ufloat( 0.249, 0.020)
        #eff_2d['FF_LT'] = ufloat( 0.214, 0.018)
        #eff_2d['FF_LL'] = ufloat( 0.396, 0.023)

        ## sigmaIEIE 25-40
        #eff_2d['FF_TT'] = ufloat( 0.181, 0.019)
        #eff_2d['FF_TL'] = ufloat( 0.244, 0.021)
        #eff_2d['FF_LT'] = ufloat( 0.237, 0.021)
        #eff_2d['FF_LL'] = ufloat( 0.338, 0.024)

        ## sigmaIEIE 40-70
        #eff_2d['FF_TT'] = ufloat( 0.225, 0.029 ) 
        #eff_2d['FF_TL'] = ufloat( 0.319, 0.032 ) 
        #eff_2d['FF_LT'] = ufloat( 0.176, 0.027 ) 
        #eff_2d['FF_LL'] = ufloat( 0.279, 0.031 ) 

        ## sigmaIEIE >70
        #eff_2d['FF_TT'] = ufloat( 0.211, 0.054)
        #eff_2d['FF_TL'] = ufloat( 0.333, 0.063)
        #eff_2d['FF_LT'] = ufloat( 0.246, 0.057)
        #eff_2d['FF_LL'] = ufloat( 0.211, 0.054)

        print 'FF_TT new = ', eff_2d['FF_TT']
        print 'FF_TL new = ', eff_2d['FF_TL']
        print 'FF_LT new = ', eff_2d['FF_LT']
        print 'FF_LL new = ', eff_2d['FF_LL']

        scan_orig = scan_fit_2d( [eff_2d_orig], data )
        scan_result = scan_fit_2d( [eff_2d], data )

        print 'Orig = ', scan_orig[0]['sum']
        print 'New  = ', scan_result[0]['sum']

        print 'N_RF_TT Orig = ', scan_orig[0]['RF_TT']
        print 'N_FR_TT Orig = ', scan_orig[0]['FR_TT']
        print 'N_FF_TT Orig = ', scan_orig[0]['FF_TT']

        print 'N_RF_TT New = ', scan_result[0]['RF_TT']
        print 'N_FR_TT New = ', scan_result[0]['FR_TT']
        print 'N_FF_TT New = ', scan_result[0]['FF_TT']

def generate_2d_efficiencies( eff_R_L_lead, eff_R_L_subl, eff_F_L_lead, eff_F_L_subl ) :

    eff = {}

    eff_R_T_lead = 1.0 - eff_R_L_lead
    eff_R_T_subl = 1.0 - eff_R_L_subl

    eff_F_T_lead = 1.0 - eff_F_L_lead
    eff_F_T_subl = 1.0 - eff_F_L_subl

    eff['RR_TT']= eff_R_T_lead*eff_R_T_subl
    eff['RR_TL']= eff_R_T_lead*eff_R_L_subl
    eff['RR_LT']= eff_R_L_lead*eff_R_T_subl
    eff['RR_LL']= eff_R_L_lead*eff_R_L_subl

    eff['RF_TT']= eff_R_T_lead*eff_F_T_subl
    eff['RF_TL']= eff_R_T_lead*eff_F_L_subl
    eff['RF_LT']= eff_R_L_lead*eff_F_T_subl
    eff['RF_LL']= eff_R_L_lead*eff_F_L_subl

    eff['FR_TT']= eff_F_T_lead*eff_R_T_subl
    eff['FR_TL']= eff_F_T_lead*eff_R_L_subl
    eff['FR_LT']= eff_F_L_lead*eff_R_T_subl
    eff['FR_LL']= eff_F_L_lead*eff_R_L_subl

    eff['FF_TT']= eff_F_T_lead*eff_F_T_subl
    eff['FF_TL']= eff_F_T_lead*eff_F_L_subl
    eff['FF_LT']= eff_F_L_lead*eff_F_T_subl
    eff['FF_LL']= eff_F_L_lead*eff_F_L_subl

    return eff
        
def get_matrix_from_dict( eff_2d ) :

    eff_matrix = [ [ eff_2d['RR_TT'], eff_2d['RF_TT'], eff_2d['FR_TT'], eff_2d['FF_TT'] ],
                   [ eff_2d['RR_TL'], eff_2d['RF_TL'], eff_2d['FR_TL'], eff_2d['FF_TL'] ],
                   [ eff_2d['RR_LT'], eff_2d['RF_LT'], eff_2d['FR_LT'], eff_2d['FF_LT'] ],
                   [ eff_2d['RR_LL'], eff_2d['RF_LL'], eff_2d['FR_LL'], eff_2d['FF_LL'] ] ]

    return eff_matrix

def scan_fit_1d( list_R_L_lead, list_R_L_subl, list_F_L_lead, list_F_L_subl, data ) :

    eff_matrices = []
    for eff_R_L_lead, eff_R_L_subl, eff_F_L_lead, eff_F_L_subl in zip( list_R_L_lead, list_R_L_subl, list_F_L_lead, list_F_L_subl  ) :

        eff_2d = generate_2d_efficiencies( eff_R_L_lead, eff_R_L_subl, eff_F_L_lead, eff_F_L_subl )

        eff_matrices.append( eff_2d )

    return scan_fit_2d( eff_matrices, data )
                         
def scan_fit_2d( matrices, data) :

    bkg_scan = []
    for eff_dict in matrices :

        eff_matrix = get_matrix_from_dict( eff_dict )

        results = solve_matrix_eq( eff_matrix, data )

        bkg_tot = results.item(1)*eff_dict['RF_TT'] + results.item(2)*eff_dict['FR_TT'] + results.item(3)*eff_dict['FF_TT']

        bkg_scan.append( { 'RF_TT' : results.item(1)*eff_dict['RF_TT'],
                           'FR_TT' : results.item(2)*eff_dict['FR_TT'], 
                           'FF_TT' : results.item(3)*eff_dict['FF_TT'], 
                            'sum'  : bkg_tot }
                       )


    return bkg_scan


def solve_matrix_eq( matrix_ntries, vector_entries ) :

    ms = []
    mn = []
    for row in matrix_ntries :
        ms_row = []
        mn_row = []
        for col in row :
            ms_row.append( col.s )
            mn_row.append( col.n )
        ms.append( ms_row )
        mn.append( mn_row )

    matrix = unumpy.umatrix( mn, ms )

    vs = []
    vn = []
    for row in vector_entries :
        vn.append( [ row.n ] )
        vs.append( [ row.s ] )

    vector = unumpy.umatrix( vn, vs )
    
    inv_matrix = None
    try :
        inv_matrix = matrix.getI()
    except :
        print 'Failed to invert matrix, aborting'
        return unumpy.umatrix( [ [1]*len(vs) ], [ [0]*len(vs) ] )

    return inv_matrix*vector

    


main()
