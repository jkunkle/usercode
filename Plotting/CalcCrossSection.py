import math
import pickle
import blue
import os
import re
from collections import OrderedDict

from argparse import ArgumentParser

from uncertainties import ufloat

parser = ArgumentParser()

parser.add_argument( '--baseDir', default=None, required=True, dest='baseDir', help='path to results' )
parser.add_argument( '--plotDir', default=None, required=True, dest='plotDir', help='name of plot dir' )
parser.add_argument( '--finalDir', default=None, required=True, dest='finalDir', help='name of final hists dir' )

options = parser.parse_args()

## FOR EB_EB
#acceptances = { 'electron' : {
#                              ('15', '25')  : ufloat( 0.1645, 0.0134 ) , 
#                              ('25', '40')  : ufloat( 0.1654, 0.0119 ) ,
#                              ('40', '70')  : ufloat( 0.2187, 0.0232 ) ,
#                              ('70', 'max') : ufloat( 0.2777, 0.0416 ) ,
#                             },
#                'muon'    : { 
#                              ('15', '25')  : ufloat( 0.2737, 0.0180 ) , 
#                              ('25', '40')  : ufloat( 0.2823, 0.0169 ) ,
#                              ('40', '70')  : ufloat( 0.3249, 0.0151 ) ,
#                              ('70', 'max') : ufloat( 0.3386, 0.0168) ,
#                             },
#}

# FOR EB_EB+EB_EE+EE_EB, > 40
acceptances = { 'electron' : {
                              ('15', '25')  : ufloat( 1.0, 0.0) , 
                              ('25', '40')  : ufloat( 1.0, 0.0) ,
                              ('40', '70')  : ufloat( 0.1596, 0.0280) ,
                              ('70', 'max') : ufloat( 0.2023, 0.0358 ) ,
                             },
                'muon'    : { 
                              ('15', '25')  : ufloat( 1.0, 0.0 ) , 
                              ('25', '40')  : ufloat( 1.0, 0.0 ) ,
                              ('40', '70')  : ufloat( 0.2645, 0.0074 ) ,
                              ('70', 'max') : ufloat( 0.2848, 0.0082 ) ,
                             },
}

comb_acceptance = { 'muon' : ufloat( 0.2662, 0.0091 ), 'electron' : ufloat( 0.1729, 0.0306) }

def main() :

    #pt_bins = [('25', '40'), ('40', '70'), ('70', 'max') ]
    pt_bins = [('40', '70'), ('70', 'max') ]
    eta_bins = [ ('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB') ]

    final_results_dir = '%s/%s'%(options.baseDir, options.finalDir )

    # define the matching regex for individual regions
    file_key_electron = 'pt_leadph12_elfullhighmt_(?P<reg1>\w{2,2})-(?P<reg2>\w{2,2}).pickle'
    file_key_muon     = 'pt_leadph12_muhighmt_(?P<reg1>\w{2,2})-(?P<reg2>\w{2,2}).pickle'

    # get the files that match the regex
    electron_results_files = get_matching_regex( os.listdir( final_results_dir ), file_key_electron )
    muon_results_files     = get_matching_regex( os.listdir( final_results_dir ), file_key_muon     )

    results = {'muon' : {}, 'electron' : {}}

    for fname, matchdic in electron_results_files :
        region = ( matchdic['reg1'], matchdic['reg2'] )
        ofile = open( '%s/%s' %( final_results_dir, fname ) )
        results['electron'][region] = pickle.load( ofile )
        ofile.close()

    for fname, matchdic in muon_results_files :
        region = ( matchdic['reg1'], matchdic['reg2'] )
        ofile = open( '%s/%s' %( final_results_dir, fname ) )
        results['muon'][region] = pickle.load( ofile )
        ofile.close()


    file_jet_muon = '%s/BackgroundEstimates/%s/jet_fake_results__muhighmt.pickle' %(options.baseDir, options.plotDir )
    file_jet_ele  = '%s/BackgroundEstimates/%s/jet_fake_results__elfullhighmt.pickle' %(options.baseDir, options.plotDir )

    results_jet = {}

    ofile_jet_muon = open( file_jet_muon )
    results_jet['muon'] = pickle.load( ofile_jet_muon )
    ofile_jet_muon.close()

    ofile_jet_ele  = open( file_jet_ele  )
    results_jet['electron'] = pickle.load( ofile_jet_ele )
    ofile_jet_ele.close()


    #calc_combined_xs( results, results_jet, pt_bins, eta_bins )

    calc_combined_xs_bins( results, results_jet, pt_bins, eta_bins, outputDir=final_results_dir )

def calc_combined_xs_bins( results_final, results_jet, pt_bins, eta_bins, outputDir=None ) :


    bin_correlations = {'statTempTight' : False, 
                        'crossCorr' : True,
                        'systBkg' : True,
                        'fakefake' : False, 
                        'systTemp' : False, 
                        'statTempLoose' : False, 
                        'statData' : False }


    all_systs = ['statTempTight', 'statTempLoose', 'systTemp', 'systBkg', 'fakefake', 'crossCorr', 'statData']

    jet_sum_el = get_simple_jet_bin_sums( results_jet['electron'], all_systs, eta_bins, pt_bins, bin_correlations )
    jet_sum_mu  = get_simple_jet_bin_sums( results_jet['muon']    , all_systs, eta_bins, pt_bins, bin_correlations )


    jet_tot_el = None
    jet_tot_mu = None

    jet_tot_el_data = None
    jet_tot_mu_data = None

    jet_tot_el_binuncorr = None
    jet_tot_mu_binuncorr = None

    jet_tot_el_bincorr = None
    jet_tot_mu_bincorr = None

    jet_tot_el_syst = None
    jet_tot_mu_syst = None

    for idx, syst in enumerate( all_systs ) :

        if idx == 0 :
            jet_tot_mu = jet_sum_mu['sum'][syst] 
            jet_tot_el = jet_sum_el['sum'][syst] 
        else :
            jet_tot_mu += ufloat( 0.0, jet_sum_mu['sum'][syst].s )
            jet_tot_el += ufloat( 0.0, jet_sum_el['sum'][syst].s )

        if bin_correlations[syst] :
            if jet_tot_el_bincorr is None :
                jet_tot_el_bincorr = jet_sum_el['sum'][syst]
                jet_tot_mu_bincorr = jet_sum_mu['sum'][syst]
            else : 
                jet_tot_el_bincorr += ufloat( 0.0, jet_sum_el['sum'][syst].s )
                jet_tot_mu_bincorr += ufloat( 0.0, jet_sum_mu['sum'][syst].s )
        else :
            if jet_tot_el_binuncorr is None :
                jet_tot_el_binuncorr = jet_sum_el['sum'][syst]
                jet_tot_mu_binuncorr = jet_sum_mu['sum'][syst]
            else : 
                jet_tot_el_binuncorr += ufloat( 0.0, jet_sum_el['sum'][syst].s )
                jet_tot_mu_binuncorr += ufloat( 0.0, jet_sum_mu['sum'][syst].s )

        if syst == 'statData' :
            jet_tot_el_data = jet_sum_el['sum'][syst]
            jet_tot_mu_data = jet_sum_mu['sum'][syst]
        else :
            if jet_tot_el_syst is None :
                jet_tot_el_syst = jet_sum_el['sum'][syst]
                jet_tot_mu_syst = jet_sum_mu['sum'][syst]
            else :
                jet_tot_el_syst += ufloat( 0.0, jet_sum_el['sum'][syst].s )
                jet_tot_mu_syst += ufloat( 0.0, jet_sum_mu['sum'][syst].s )
    

    print 'Jet total mu = ', jet_tot_mu
    print 'Jet total el = ', jet_tot_el

    summed_mu = {}
    summed_el = {}

    summed_mu['JetFake']          = { 'sum' : jet_tot_mu }
    summed_el['JetFake']          = { 'sum' : jet_tot_el }
    summed_mu['JetFakeStat']      = { 'sum' : jet_tot_mu_data }
    summed_el['JetFakeStat']      = { 'sum' : jet_tot_el_data }

    summed_mu['JetFakeSyst']      = { 'sum' : jet_tot_mu_syst }
    summed_el['JetFakeSyst']      = { 'sum' : jet_tot_el_syst }

    summed_mu['JetFakeBinCorr']   = { 'sum' : jet_tot_mu_bincorr }
    summed_el['JetFakeBinCorr']   = { 'sum' : jet_tot_el_bincorr }

    summed_mu['JetFakeBinUncorr'] = { 'sum' : jet_tot_mu_binuncorr }
    summed_el['JetFakeBinUncorr'] = { 'sum' : jet_tot_el_binuncorr }

    retrieve_samples = ['Zgg', 'Data', 'EleFake']

    summed_mu['Zgg']  = get_summed_sample( results_final['muon'],  'Zgg' , pt_bins, eta_bins, isCorr=True )
    summed_mu['ZggStat']  = get_summed_sample( results_final['muon'],  'ZggNoSyst' , pt_bins, eta_bins, isCorr=False )
    summed_mu['Wgg']  = get_summed_sample( results_final['muon'],  'Wgg' , pt_bins, eta_bins, isCorr=True )
    summed_mu['Data'] = get_summed_sample( results_final['muon'],  'Data', pt_bins, eta_bins, isCorr=False )

    print summed_mu['Zgg']
    print summed_mu['ZggStat']

    summed_el['Zgg']     = get_summed_sample( results_final['electron'],  'Zgg'    , pt_bins, eta_bins, isCorr=True )
    summed_el['ZggStat']  = get_summed_sample( results_final['electron'],  'ZggNoSyst', pt_bins, eta_bins, isCorr=False )
    summed_el['Wgg']     = get_summed_sample( results_final['electron'],  'Wgg'    , pt_bins, eta_bins, isCorr=True )
    summed_el['Data']    = get_summed_sample( results_final['electron'],  'Data'   , pt_bins, eta_bins, isCorr=False )
    summed_el['EleFake'] = get_summed_sample( results_final['electron'],  'EleFake', pt_bins, eta_bins, isCorr=False )

    summed_mu['ZggSyst'] = make_uncert_compliment( summed_mu['Zgg'], summed_mu['ZggStat'], isCorr=True )
    summed_el['ZggSyst'] = make_uncert_compliment( summed_el['Zgg'], summed_el['ZggStat'], isCorr=True )

    bkg_el = summed_el['Zgg']['sum']+summed_el['EleFake']['sum']+summed_el['JetFake']['sum']
    bkg_mu = summed_mu['Zgg']['sum']+summed_mu['JetFake']['sum']

    lumi = ufloat( 19.4, 19.4*0.026 )

    exp_mu = bkg_mu + summed_mu['Wgg']['sum']
    exp_el = bkg_el + summed_el['Wgg']['sum']
    xs_mu_sig =  (ufloat( exp_mu.n, math.sqrt(exp_mu.n) ) - bkg_mu)/ ( comb_acceptance['muon'] * lumi )
    xs_el_sig =  (ufloat(exp_el.n, math.sqrt(exp_el.n) ) - bkg_el )/ ( comb_acceptance['electron'] * lumi )
    xs_mu = ( summed_mu['Data']['sum'] - bkg_mu )/ ( comb_acceptance['muon'] * lumi )
    xs_el = ( summed_el['Data']['sum'] - bkg_el )/ ( comb_acceptance['electron'] * lumi )

    print 'Muon, N Data = %d, N Sig = %f, n Bkg = %s '      %( summed_mu['Data']['sum'].n, summed_mu['Wgg']['sum'].n, bkg_mu )
    print 'Electron , N Data = %d, N Sig = %f, n Bkg = %s ' %( summed_el['Data']['sum'].n, summed_el['Wgg']['sum'].n, bkg_el )
    print 'S/sigma(B), mu =  %f ' %( summed_mu['Wgg']['sum'].n / bkg_mu.s )
    print 'S/sigma(B), el =  %f ' %( summed_el['Wgg']['sum'].n / bkg_el.s )
    print 'xs_mu_sig = %s, frac unc = %f' %( xs_mu_sig, xs_mu_sig.s/xs_mu_sig.n)
    print 'xs_el_sig = %s, frac unc = %f' %( xs_el_sig, xs_el_sig.s/xs_el_sig.n)
    print 'xs_mu = %s' %xs_mu
    print 'xs_el = %s' %xs_el

    xs_systs_mu = {'components' : { 'Data' : summed_mu['Data']['sum'], 
                                   'JetFakeStat' : summed_mu['JetFakeStat'], 'JetFakeSyst' : summed_mu['JetFakeSyst'],
                                   'JetFakeBinCorr' : summed_mu['JetFakeBinCorr'], 'JetFakeBinUncorr' : summed_mu['JetFakeBinUncorr'],
                                   'ZggStat' : summed_mu['ZggStat']['sum'],'ZggSyst' : summed_mu['ZggSyst']['sum'], 
                                   'EleFake' : ufloat(0,0), 'Acc' : comb_acceptance['muon'], 'lumi' : lumi } }

    xs_systs_el = {'components' : { 'Data' : summed_el['Data']['sum'], 
                                   'JetFakeStat' : summed_el['JetFakeStat'], 'JetFakeSyst' : summed_el['JetFakeSyst'],
                                   'JetFakeBinCorr' : summed_el['JetFakeBinCorr'], 'JetFakeBinUncorr' : summed_el['JetFakeBinUncorr'],
                                   'ZggStat' : summed_el['ZggStat']['sum'],'ZggSyst' : summed_el['ZggSyst']['sum'], 
                                   'EleFake' : summed_el['EleFake']['sum'], 'Acc' : comb_acceptance['electron'], 'lumi' : lumi } }

    xs_systs_mu['systs'] = {}
    xs_systs_el['systs'] = {}

    xs_systs_mu['systs']['Data'] = ( summed_mu['Data']['sum'] - ufloat( bkg_mu.n, 0.0) ) / ( ufloat(comb_acceptance['muon'].n, 0.0 ) * ufloat( lumi.n, 0.0 ) )
    xs_systs_el['systs']['Data'] = ( summed_el['Data']['sum'] - ufloat( bkg_el.n, 0.0) ) / ( ufloat(comb_acceptance['electron'].n, 0.0 ) * ufloat( lumi.n, 0.0 ) )

    xs_systs_mu['systs']['JetFakeStat'] = ( ufloat(summed_mu['Data']['sum'].n, 0.0 ) - summed_mu['JetFakeStat']['sum'] - ufloat( summed_mu['Zgg']['sum'].n, 0.0) ) / ( ufloat(comb_acceptance['muon'].n, 0.0 ) * ufloat( lumi.n, 0.0 ) )
    xs_systs_el['systs']['JetFakeStat'] = ( ufloat(summed_el['Data']['sum'].n, 0.0 ) - summed_el['JetFakeStat']['sum'] - ufloat( summed_el['Zgg']['sum'].n, 0.0)  - ufloat( summed_el['EleFake']['sum'].n, 0.0)  ) / ( ufloat(comb_acceptance['electron'].n, 0.0 ) * ufloat( lumi.n, 0.0 ) )

    xs_systs_mu['systs']['JetFakeSyst'] = ( ufloat(summed_mu['Data']['sum'].n, 0.0 ) - summed_mu['JetFakeSyst']['sum'] - ufloat( summed_mu['Zgg']['sum'].n, 0.0) ) / ( ufloat(comb_acceptance['muon'].n, 0.0 ) * ufloat( lumi.n, 0.0 ) )
    xs_systs_el['systs']['JetFakeSyst'] = ( ufloat(summed_el['Data']['sum'].n, 0.0 ) - summed_el['JetFakeSyst']['sum'] - ufloat( summed_el['Zgg']['sum'].n, 0.0)  - ufloat( summed_el['EleFake']['sum'].n, 0.0)  ) / ( ufloat(comb_acceptance['electron'].n, 0.0 ) * ufloat( lumi.n, 0.0 ) )

    xs_systs_mu['systs']['ZggStat'] = ( ufloat(summed_mu['Data']['sum'].n, 0.0 ) - summed_mu['ZggStat']['sum'] - ufloat( summed_mu['JetFake']['sum'].n, 0.0) ) / ( ufloat(comb_acceptance['muon'].n, 0.0 ) * ufloat( lumi.n, 0.0 ) )
    xs_systs_el['systs']['ZggStat'] = ( ufloat(summed_el['Data']['sum'].n, 0.0 ) - summed_el['ZggStat']['sum'] - ufloat( summed_el['JetFake']['sum'].n, 0.0)  - ufloat( summed_el['EleFake']['sum'].n, 0.0)  ) / ( ufloat(comb_acceptance['electron'].n, 0.0 ) * ufloat( lumi.n, 0.0 ) )

    xs_systs_mu['systs']['ZggSyst'] = ( ufloat(summed_mu['Data']['sum'].n, 0.0 ) - summed_mu['ZggSyst']['sum'] - ufloat( summed_mu['JetFake']['sum'].n, 0.0) ) / ( ufloat(comb_acceptance['muon'].n, 0.0 ) * ufloat( lumi.n, 0.0 ) )
    xs_systs_el['systs']['ZggSyst'] = ( ufloat(summed_el['Data']['sum'].n, 0.0 ) - summed_el['ZggSyst']['sum'] - ufloat( summed_el['JetFake']['sum'].n, 0.0)  - ufloat( summed_el['EleFake']['sum'].n, 0.0)  ) / ( ufloat(comb_acceptance['electron'].n, 0.0 ) * ufloat( lumi.n, 0.0 ) )

    xs_systs_mu['systs']['EleFake'] = ufloat( xs_mu.n, 0.0 )
    xs_systs_el['systs']['EleFake'] = ( ufloat(summed_el['Data']['sum'].n, 0.0 ) - summed_el['EleFake']['sum'] - ufloat( summed_el['JetFake']['sum'].n, 0.0)  - ufloat( summed_el['Zgg']['sum'].n, 0.0)  ) / ( ufloat(comb_acceptance['electron'].n, 0.0 ) * ufloat( lumi.n, 0.0 ) )

    xs_systs_mu['systs']['Acc'] = ( ufloat(summed_mu['Data']['sum'].n, 0.0 ) - ufloat( summed_mu['Zgg']['sum'].n, 0.0) - ufloat( summed_mu['JetFake']['sum'].n, 0.0) ) / ( comb_acceptance['muon'] * ufloat( lumi.n, 0.0 ) )
    xs_systs_el['systs']['Acc'] = ( ufloat(summed_el['Data']['sum'].n, 0.0 ) - ufloat( summed_el['Zgg']['sum'].n, 0.0) - ufloat( summed_el['JetFake']['sum'].n, 0.0)  - ufloat( summed_el['EleFake']['sum'].n, 0.0)  ) / ( comb_acceptance['electron'] * ufloat( lumi.n, 0.0 ) )

    ch_correlations  = {'Data'    : False, 
                        'JetFakeStat' : False, 
                        'JetFakeSyst' : True, 
                        'ZggStat'     : False, 
                        'ZggSyst'     : True, 
                        'EleFake' : False, 
                        'Acc'     : True 
                       }

    xs_calc = blue.Calculator()


    meas_values = [xs_mu.n, xs_el.n]
    xs_calc.SetMeasurementValues( meas_values )

    # make BLUE calculators for each separate uncertainty
    calc_indiv = {}
    for syst in xs_systs_mu['systs'].keys() :
        calc_indiv[syst] = blue.Calculator()
        calc_indiv[syst].SetMeasurementValues( meas_values )


    n_ch = 2
    for syst, is_corr in ch_correlations.iteritems() :

        matrix  = []
        for i in range( 0, n_ch ) :
            list_i = [0]*n_ch
            for j in range( 0, n_ch ) :
                entry  = xs_systs_mu['systs'][syst].s*xs_systs_el['systs'][syst].s

                if i != j and not is_corr :
                    entry = 0

                list_i[j]  = entry

            matrix.append( list_i )

        xs_calc.AddErrorMatrix( matrix )
        if syst in calc_indiv :
            calc_indiv[syst].AddErrorMatrix( matrix)

    combined_value = xs_calc.CalculateCombinedValue()
    combined_error = xs_calc.CalculateCombinedUncertainty()

    combined_alphas = xs_calc.GetAlphas()
    for icalc in calc_indiv.values() :
        icalc.SetAlphas( combined_alphas )

    comb_results = {}
    comb_results['combined'] = ufloat( combined_value, combined_error )
    comb_results['isCorr'] = {}

    for unc, icalc in calc_indiv.iteritems() :

        comb_results['isCorr'][unc] = ch_correlations[unc]

        value = icalc.CalculateCombinedValue()
        uncert= icalc.CalculateCombinedUncertainty()

        comb_results[unc] = ufloat( value, uncert )

    print 'Combined xs = %s' %( ufloat( combined_value, combined_error ) )

    if outputDir is not None :
        output_results = {}
        output_results['channels'] = {'muon' : {}, 'electron' : {} }

        output_results['channels']['muon']['JetSum'] = jet_sum_mu
        output_results['channels']['electron']['JetSum'] = jet_sum_el

        output_results['channels']['muon']['BkgSum'] = summed_mu
        output_results['channels']['electron']['BkgSum'] = summed_el

        output_results['channels']['muon']['CrossSection'] = xs_systs_mu
        output_results['channels']['electron']['CrossSection'] = xs_systs_el

        output_results['combination'] = comb_results

        outfile = open( '%s/%s' %( outputDir, 'cross_section_details.pickle' ), 'w' )
        pickle.dump( output_results, outfile )
        outfile.close()

#def calc_combined_xs( results_final, results_jet, pt_bins, eta_bins ) :
#
#    all_vars = ['SigmaIEIEFits', 'ChHadIsoFits', 'PhoIsoFits']
#
#    bin_correlations = {'statTempTight' : False, 
#                        'crossCorr' : True,
#                        'systBkg' : True,
#                        'fakefake' : False, 
#                        'systTemp' : False, 
#                        'statTempLoose' : False, 
#                        'statData' : False }
#
#    var_correlations = {'systTemp' : False, 'systBkg' : True, 'statTempTight' : True, 'statTempLoose' : True, 'statData' : False, 'fakefake' : False, 'crossCorr' : True}
#    ch_correlations  = {'systTemp' : True, 'systBkg' : True, 'statTempTight' : True, 'statTempLoose' : True, 'statData' : False, 'fakefake' : True, 'crossCorr' : True}
#
#    indiv_entries = results_jet.values()[0]['individual'].keys()
#
#    jet_sum_ele = get_jet_bin_sums( results_jet['electron'], existing_vars, all_systs, eta_bins, pt_bins, bin_correlations )
#    jet_sum_mu  = get_jet_bin_sums( results_jet['muon']    , existing_vars, all_systs, eta_bins, pt_bins, bin_correlations )
#
#    jet_result_ele = combine_jet_vars( jet_sum_ele, existing_vars, all_systs, var_correlations )
#    jet_result_mu  = combine_jet_vars( jet_sum_mu , existing_vars, all_systs, var_correlations )
#
#    print 'Jet total ELe = %s' %jet_result_ele
#    print 'Jet total Mu = %s' %jet_result_mu
#
#    summed_mu = {}
#    summed_el = {}
#
#    summed_mu['JetFake'] = jet_result_mu['combined']
#    summed_el['JetFake'] = jet_result_ele['combined']
#
#    retrieve_samples = ['Zgg', 'Data', 'EleFake']
#
#    summed_mu['Zgg']        = get_summed_sample( results_final['muon'],  'Zgg'       , pt_bins, eta_bins, isCorr=False )
#    summed_mu['ZggNoSyst']  = get_summed_sample( results_final['muon'],  'ZggNoSyst' , pt_bins, eta_bins, isCorr=False )
#    summed_mu['Wgg']        = get_summed_sample( results_final['muon'],  'Wgg'       , pt_bins, eta_bins, isCorr=True )
#    summed_mu['Data']       = get_summed_sample( results_final['muon'],  'Data'      , pt_bins, eta_bins, isCorr=False )
#
#    summed_el['Zgg']        = get_summed_sample( results_final['electron'],  'Zgg'      , pt_bins, eta_bins, isCorr=False )
#    summed_el['ZggNoSyst']  = get_summed_sample( results_final['electron'],  'ZggNoSyst', pt_bins, eta_bins, isCorr=False )
#    summed_el['Wgg']        = get_summed_sample( results_final['electron'],  'Wgg'      , pt_bins, eta_bins, isCorr=True )
#    summed_el['Data']       = get_summed_sample( results_final['electron'],  'Data'     , pt_bins, eta_bins, isCorr=False )
#    summed_el['EleFake']    = get_summed_sample( results_final['electron'],  'EleFake'  , pt_bins, eta_bins, isCorr=False )
#
#    summed_mu['ZggNoStat'] = make_uncert_compliment( summed_mu['Zgg'], summed_mu['ZggNoSyst'], isCorr=True )
#    summed_el['ZggNoStat'] = make_uncert_compliment( summed_el['Zgg'], summed_el['ZggNoSyst'], isCorr=True )
#
#    print summed_mu
#    print summed_el
#
#    bkg_el = summed_el['Zgg']+summed_el['EleFake']+summed_el['JetFake']
#    bkg_mu = summed_mu['Zgg']+summed_mu['JetFake']
#
#    lumi = ufloat( 19.4, 19.4*0.026 )
#    xs_mu_sig =  ufloat( summed_mu['Wgg'].n, math.sqrt(summed_mu['Wgg'].n))/ ( comb_acceptance['muon'] * lumi )
#    xs_el_sig =  ufloat( summed_el['Wgg'].n, math.sqrt(summed_el['Wgg'].n))/ ( comb_acceptance['electron'] * lumi )
#    xs_mu = ( summed_mu['Data'] - bkg_mu )/ ( comb_acceptance['muon'] * lumi )
#    xs_el = ( summed_el['Data'] - bkg_el )/ ( comb_acceptance['electron'] * lumi )
#
#    print 'xs_mu_sig = %s, frac unc = %f' %( xs_mu_sig, xs_mu_sig.s/xs_mu_sig.n)
#    print 'xs_el_sig = %s, frac unc = %f' %( xs_el_sig, xs_el_sig.s/xs_el_sig.n)
#    print 'xs_mu = %s' %xs_mu
#    print 'xs_el = %s' %xs_el
#
#    xs_total = combine_channels( [jet_result_mu, jet_result_ele], all_systs, ch_correlations )
#    print 'combined jet fake = ', jet_fake_total




def get_summed_sample( hist_entries, sample, pt_bins, eta_bins, isCorr=False ) :

    results = {}
    results['sum'] = ufloat( 0.0, 0.0)
    results['bins'] = {}
    results['isCorr'] = isCorr

    # first get the maximum bin from the histogram for later use
    bin_maxs = []
    for bidx, binfo in hist_entries.values()[0]['detail'][sample]['bins'].iteritems()  :
        bin_maxs.append( int( binfo['max'] ) )
    max_bin = max( bin_maxs )

    for reg1, reg2 in eta_bins :

        eta_bin = (reg1, reg2)
        for ptmin, ptmax  in pt_bins :

            reg_bin = ( reg1, reg2, ptmin, ptmax )

            bin_idx = -1

            # find the histogram bin matching this bin
            for bidx, binfo in hist_entries[eta_bin]['detail'][sample]['bins'].iteritems()  :

                bmin = int(binfo['min'])
                bmax = int(binfo['max'])

                strbinmax = str(bmax)
                if bmax == max_bin :
                    strbinmax = 'max'

                if str(bmin) == ptmin and strbinmax == ptmax :
                    bin_idx = bidx 
                    break

            data = hist_entries[eta_bin]['detail'][sample]['bins'][bin_idx]['val']

            if isCorr :
                results['sum'] = ufloat( results['sum'].n + data.n, results['sum'].s + data.s )
            else :
                results['sum'] += data

            results['bins'][reg_bin] = data

    return results

def make_uncert_compliment( total_samp, remove_samp, isCorr=False ) :

    out_results = {}
    out_results['sum'] = ufloat( 0.0, 0.0 )
    out_results['isCorr'] = isCorr
    out_results['bins'] = {}

    for reg_bin, total_val in total_samp['bins'].iteritems() :

        remove_val = remove_samp['bins'][reg_bin]

        comp_err = math.sqrt(total_val.s*total_val.s - remove_val.s*remove_val.s)

        comp = ufloat( total_val.n, comp_err )
        out_results['bins'][reg_bin] = comp

        if isCorr : 
            out_results['sum'] = ufloat( out_results['sum'].n + comp.n, out_results['sum'].s + comp.s )
        else :
            out_results['sum'] += comp

    return out_results

def combine_channels( channel_results, systs, ch_correlations  ) :

    calc_comb  = blue.Calculator() 

    meas_values = []
    for chres in channel_results :
        meas_values.append( chres[systs[0]].n )

    calc_comb.SetMeasurementValues( meas_values )

    n_ch = len( channel_results)
    for syst in systs :

        is_corr = ch_correlations[syst]

        matrix  = []
        for i in range( 0, n_ch ) :
            list_i = [0]*n_ch
            for j in range( 0, n_ch ) :
                entry  = channel_results[i][syst].s*channel_results[j][syst].s

                if i != j and not is_corr :
                    entry = 0

                list_i[j]  = entry

            matrix.append( list_i )

        calc_comb.AddErrorMatrix( matrix )

    combined_value = calc_comb.CalculateCombinedValue()
    combined_error = calc_comb.CalculateCombinedUncertainty()

    return ufloat( combined_value, combined_error )


def combine_jet_vars( jet_sum, vars, systs, var_correlations  ) :

    calc_comb  = blue.Calculator() 

    meas_values  = []

    for var in vars :
        # grab the central value from any of the entries
        meas_values.append( jet_sum[var].values()[0].n )

    calc_comb.SetMeasurementValues( meas_values )

    # make BLUE calculators for each separate uncertainty
    calc_indiv = {}
    for syst in systs :
        calc_indiv[syst] = blue.Calculator()
        calc_indiv[syst].SetMeasurementValues( meas_values )

    n_var = len( vars )
    for syst in systs :

        is_corr = var_correlations[syst]

        matrix  = []
        for i in range( 0, n_var ) :
            list_i = [0]*n_var
            for j in range( 0, n_var ) :
                entry  = jet_sum[vars[i]][syst].s*jet_sum[vars[j]][syst].s

                if i != j and not is_corr :
                    entry = 0

                list_i[j]  = entry

            matrix.append( list_i )

        calc_comb.AddErrorMatrix( matrix )
        if syst in calc_indiv :
            calc_indiv[syst].AddErrorMatrix( matrix)

    combined_value = calc_comb.CalculateCombinedValue()
    combined_error = calc_comb.CalculateCombinedUncertainty()

    combined_alphas = calc_comb.GetAlphas()
    for icalc in calc_indiv.values() :
        icalc.SetAlphas( combined_alphas )

    results = {}
    results['combined'] = ufloat( combined_value, combined_error )

    for unc, icalc in calc_indiv.iteritems() :

        value = icalc.CalculateCombinedValue()
        uncert= icalc.CalculateCombinedUncertainty()

        results[unc] = ufloat( value, uncert )


    return results

def get_simple_jet_bin_sums( results, systs, eta_bins, pt_bins, bin_correlations ) :

    jet_sum = {}
    jet_sum['bins'] = {}
    jet_sum['sum'] = {}
    jet_sum['isCorr'] = {}
    for syst in systs :
        jet_sum ['sum'][syst] = ufloat(0.0, 0.0 )
        jet_sum['isCorr'][syst] = bin_correlations[syst]

    for r1, r2 in eta_bins :
        for ptmin, ptmax in pt_bins :

            reg_bin = ( r1, r2, ptmin, ptmax )

            jet_sum['bins'][reg_bin] = {}

            for syst in systs :

                syst_val = results['individual'][syst]['sum'][reg_bin].get('result', None )
                if syst_val is None :
                    print 'WARNING, systematic does not exist ', syst
                else :
                    if bin_correlations[syst] :
                        # if correlated the uncertainty is a linear sum
                        jet_sum['sum'][syst] = ufloat( jet_sum['sum'][syst].n + syst_val.n, jet_sum['sum'][syst].s + syst_val.s) 
                    else :
                        jet_sum['sum'][syst] += syst_val
                jet_sum['bins'][reg_bin][syst] = syst_val

    return jet_sum


def get_jet_bin_sums( results, vars, systs, eta_bins, pt_bins, bin_correlations ) :

    jet_sum = {}
    for var in vars :
        jet_sum [var] = {}
        for syst in systs :
            jet_sum [var][syst] = ufloat(0.0, 0.0 )

    for r1, r2 in eta_bins :
        for ptmin, ptmax in pt_bins :

            reg_bin = ( r1, r2, ptmin, ptmax )

            for var in vars:

                for syst in systs :

                    syst_val = results['individual'][var]['sum'][reg_bin]['result'].get( syst, None )
                    if syst_val is None :
                        print 'WARNING, systematic does not exist ', syst
                    else :
                        if bin_correlations[syst] :
                            # if correlated the uncertainty is a linear sum
                            jet_sum[var][syst] = ufloat( jet_sum[var][syst].n + syst_val.n, jet_sum[var][syst].s + syst_val.s) 
                        else :
                            jet_sum[var][syst] += syst_val

    return jet_sum



def calc_xs_old( results ) :

    pt_bins = ['15', '25', '40', '70', 'max']
    #pt_bins = ['40', '70', 'max']

    lumi = ufloat( 19.4, 19.4*0.026 )
    #lumi = ufloat( 19.4, 0.0 )
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

            data = res['detail']['Data']['bins'][str(idx+1)]['val']

            bkg = ufloat( 0.0, 0.0 )
            sig = ufloat( 0.0, 0.0 )

            bkg = bkg + res['detail']['Zgg']['bins'][str(idx+1)]['val']
            bkg = bkg + res['detail']['JetFake']['bins'][str(idx+1)]['val']
            print '********************FIX*****************'
            #bkg = bkg + res['detail']['OtherDiPhoton']['bins'][str(idx+1)]['val']

            if ch=='electron' :
                bkg = bkg + res['detail']['EleFake']['bins'][str(idx+1)]['val']

            sig = sig + res['detail']['Wgg']['bins'][str(idx+1)]['val']
            sig = ufloat( sig.n, math.sqrt( sig.n ) )

            bkg = ufloat( bkg.n, 0.0 )

            #data = ufloat( data.n , 0.0 )

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
    cross_section_tot = ufloat( 0.0, 0.0 )
    cross_section_tot_exp = ufloat( 0.0, 0.0 )
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
            if ptmin == '15' :
                cross_section_tot = cross_section_tot + cross_section
                cross_section_tot_exp = cross_section_tot_exp   + cross_section_exp

    print 'Total Expected cross section = %s' %cross_section_tot_exp
    print 'Total Cross section = %s' %cross_section_tot


        
    ofile = open( '%s/cross_section_results.pickle' %(options.baseDir ), 'w' )

    pickle.dump(xs_data, ofile )

    ofile.close()

def get_matching_regex( full_list, match ) :
    
    matches = []

    for obj in full_list :
        res = re.match( match, obj )

        if res is not None :
            matches.append( ( obj, res.groupdict() ) )

    return matches







main()
