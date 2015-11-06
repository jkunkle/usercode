import math
import pickle
import blue
import os
import re
from collections import OrderedDict

from argparse import ArgumentParser

from uncertainties import ufloat

parser = ArgumentParser()

parser.add_argument( '--zgg'     , default=False, action='store_true', required=False, dest='zgg', help='make Zgg cross section' )
parser.add_argument( '--ratio'   , default=False, action='store_true', required=False, dest='ratio', help='make Wgg and Zgg cross sections and their ratios' )


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

acc_el = 0.1721
acc_mu = 0.2675
comb_acceptance =     { 'muon' : {
                                    'stat'   : ufloat( acc_mu, acc_mu*0.0055 ), 
                                    'Channel': ufloat( acc_mu, acc_mu*0.0040 ), 
                                    'Photon' : ufloat( acc_mu, acc_mu*0.0244 ), 
                                    'Theory' : ufloat( acc_mu, acc_mu*0.0162 ), 
                                 },
                       'electron' : {
                                    'stat'   : ufloat( acc_el, acc_el*0.0041),
                                    'Channel': ufloat( acc_el, acc_el*0.1689), 
                                    'Photon' : ufloat( acc_el, acc_el*0.0244 ), 
                                    'Theory' : ufloat( acc_el, acc_el*0.0155 ), 
                                    }
                     }

acc_el_zgg = 0.1765
acc_mu_zgg = 0.2555

comb_acceptance_zgg =  { 'muon' : {
                                    'stat'   : ufloat( acc_mu_zgg, acc_mu_zgg*0.0078 ), 
                                    'Channel': ufloat( acc_mu_zgg, acc_mu_zgg*0.0122 ), 
                                    'Photon' : ufloat( acc_mu_zgg, acc_mu_zgg*0.0296 ), 
                                    'Theory' : ufloat( acc_mu_zgg, acc_mu_zgg*0.0230 ), 
                                 },
                       'electron' : {
                                    'stat'   : ufloat( acc_el_zgg, acc_el_zgg*0.0064),
                                    'Channel': ufloat( acc_el_zgg, acc_el_zgg*0.0332), 
                                    'Photon' : ufloat( acc_el_zgg, acc_el_zgg*0.0289 ), 
                                    'Theory' : ufloat( acc_el_zgg, acc_el_zgg*0.0230 ), 
                                    }
                     }


def main() :

    baseDirWgg  = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2015_10_13/'
    plotDirWgg  = 'PlotsUnblindMCNDWithPhoWithCorrNoDiffUncNewOneBin'
    finalDirWgg = 'FinalPlotsPlotsUnblindMCNDWithPhoWithCorrNoDiffUncNewOneBin'

    baseDirZgg  = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2015_10_15/'
    plotDirZgg  = 'PlotsUnblindZggNewOneBin'
    finalDirZgg = 'FinalPlotsOneBin'

    #baseDirZgg  = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2015_10_15/'
    #plotDirZgg  = 'PlotsUnblindZggNew'
    #finalDirZgg = 'FinalPlots'

    #baseDirZgg  = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2015_11_03/'
    #plotDirZgg  = 'PlotsUnblindZggOneBin25'
    #finalDirZgg = 'FinalPlotsOneBin25'

    #pt_bins = [('25', '40'), ('40', '70'), ('70', 'max') ]
    #pt_bins = [('40', '70'), ('70', 'max') ]
    pt_bins_wgg = [('25', 'max') ]
    pt_bins_zgg = [('15', 'max') ]
    #pt_bins_zgg = [('25', 'max') ]

    #pt_bins_zgg = [('15', '25'), ('25', '40'), ('40', 'max')]

    eta_bins = [ ('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB') ]

    final_results_dir_wgg = '%s/%s'%(baseDirWgg, finalDirWgg )
    final_results_dir_zgg = '%s/%s'%(baseDirZgg, finalDirZgg )

    # define the matching regex for individual regions
    file_key_electron_wgg = 'pt_leadph12_elfullhighmt_(?P<reg1>\w{2,2})-(?P<reg2>\w{2,2}).pickle'
    file_key_muon_wgg     = 'pt_leadph12_muhighmt_(?P<reg1>\w{2,2})-(?P<reg2>\w{2,2}).pickle'
    file_key_electron_zgg = 'pt_leadph12_elZgg_(?P<reg1>\w{2,2})-(?P<reg2>\w{2,2}).pickle'
    file_key_muon_zgg     = 'pt_leadph12_muZgg_(?P<reg1>\w{2,2})-(?P<reg2>\w{2,2}).pickle'

    # get the files that match the regex
    electron_results_files_wgg = get_matching_regex( os.listdir( final_results_dir_wgg ), file_key_electron_wgg )
    muon_results_files_wgg     = get_matching_regex( os.listdir( final_results_dir_wgg ), file_key_muon_wgg     )

    electron_results_files_zgg = get_matching_regex( os.listdir( final_results_dir_zgg ), file_key_electron_zgg )
    muon_results_files_zgg     = get_matching_regex( os.listdir( final_results_dir_zgg ), file_key_muon_zgg     )

    results_wgg = {'muon' : {}, 'electron' : {}}
    results_zgg = {'muon' : {}, 'electron' : {}}

    results_wgg['electron'] = collect_match_results_from_pickle( final_results_dir_wgg, electron_results_files_wgg )
    results_wgg['muon']     = collect_match_results_from_pickle( final_results_dir_wgg, muon_results_files_wgg     )

    results_zgg['electron'] = collect_match_results_from_pickle( final_results_dir_zgg, electron_results_files_zgg )
    results_zgg['muon']     = collect_match_results_from_pickle( final_results_dir_zgg, muon_results_files_zgg     )

    plotDirWgg = '%s/BackgroundEstimates/%s'%(baseDirWgg, plotDirWgg )
    plotDirZgg = '%s/BackgroundEstimates/%s'%(baseDirZgg, plotDirZgg )

    file_jet_muon_wgg = '%s/jet_fake_results__muhighmt.pickle'     %(plotDirWgg )
    file_jet_ele_wgg  = '%s/jet_fake_results__elfullhighmt.pickle' %(plotDirWgg )

    file_jet_muon_zgg = '%s/jet_fake_results__muZgg.pickle'    %(plotDirZgg )
    file_jet_ele_zgg  = '%s/jet_fake_results__elZgg.pickle'    %(plotDirZgg )


    results_jet_wgg = {}
    results_jet_zgg = {}

    results_jet_wgg['muon']     = get_dic_from_pickle( file_jet_muon_wgg )
    results_jet_wgg['electron'] = get_dic_from_pickle( file_jet_ele_wgg )

    results_jet_zgg['muon']     = get_dic_from_pickle( file_jet_muon_zgg )
    results_jet_zgg['electron'] = get_dic_from_pickle( file_jet_ele_zgg )

    comb_wgg = calc_combined_xs_bins( results_wgg, results_jet_wgg, pt_bins_wgg, eta_bins, zgg=False, plotDir=plotDirWgg, outputDir=final_results_dir_wgg )
    comb_zgg = calc_combined_xs_bins( results_zgg, results_jet_zgg, pt_bins_zgg, eta_bins, zgg=True , plotDir=plotDirZgg, outputDir=final_results_dir_zgg )


    print 'COMB_Wgg' 
    print comb_wgg['combination']
    print 'COMB_Zgg' 
    print comb_zgg['combination']

    print 'Ratio = %s ' %( comb_wgg['combination']['systs']['statData']/comb_zgg['combination']['systs']['statData'] )

def calc_combined_xs_bins( results_final, results_jet, pt_bins, eta_bins, zgg=False, plotDir=None, outputDir=None ) :


    bin_correlations = {'statTempTight' : False, 
                        'crossCorr' : True,
                        'systBkg' : True,
                        'fakefake' : False, 
                        'systTemp' : False, 
                        'statTempLoose' : False, 
                        'statData' : False }

    all_systs = ['statTempTight', 'statTempLoose', 'systTemp', 'systBkg', 'fakefake', 'crossCorr', 'statData']

    jet_sum_el = get_simple_jet_bin_sums( results_jet['electron'], all_systs, eta_bins, pt_bins, bin_correlations )
    jet_sum_mu = get_simple_jet_bin_sums( results_jet['muon']    , all_systs, eta_bins, pt_bins, bin_correlations )

    summed_el = collect_jet_systs( jet_sum_el, all_systs, bin_correlations )
    summed_mu = collect_jet_systs( jet_sum_mu, all_systs, bin_correlations )

    # electron fakes
    if not zgg :

        file_el = '%s/electron_fake_results__elfullhighmt.pickle' %(plotDir )
        ofile_el = open( file_el )
        results_el = pickle.load( ofile_el )
        ofile_el.close()

        file_jet_subl = '%s/jet_fake_results__elfullhighmtinvpixsubl.pickle' %(plotDir )
        file_jet_lead = '%s/jet_fake_results__elfullhighmtinvpixlead.pickle' %(plotDir )

        ofile_subl = open( file_jet_subl )
        ofile_lead = open( file_jet_lead )

        results_jet_lead = pickle.load( ofile_lead )
        results_jet_subl = pickle.load( ofile_subl )

        ofile_lead.close()
        ofile_subl.close()

        jet_sum = {'lead' : {}, 'subl' : {}, 'nom' : {} }
        sb_data = {'lead' : {}, 'subl' : {} }
        ffs     = {'lead' : {}, 'subl' : {} }

        combined_fake = {}
        for eb in eta_bins :
            jet_sum['lead'][eb] = collect_jet_systs( get_simple_jet_bin_sums( results_jet_lead, all_systs, [eb], pt_bins, bin_correlations ), all_systs, bin_correlations )
            jet_sum['subl'][eb] = collect_jet_systs( get_simple_jet_bin_sums( results_jet_subl, all_systs, [eb], pt_bins, bin_correlations ), all_systs, bin_correlations )
            jet_sum['nom' ][eb] = collect_jet_systs( get_simple_jet_bin_sums( results_jet['electron'], all_systs, [eb], pt_bins, bin_correlations ), all_systs, bin_correlations )

            sb_data['lead'][eb] = ufloat(0,0)
            sb_data['subl'][eb] = ufloat(0,0)
            ffs['lead'][eb] = ufloat(0,0)
            ffs['subl'][eb] = ufloat(0,0)
            for ptmin, ptmax in pt_bins :
                res_bin = (eb[0],eb[1],ptmin,ptmax)
                ana_bins_lead = [x for x in results_el['details']['lead'][res_bin].keys() if isinstance(x, tuple ) ]
                for ab in ana_bins_lead :
                    sb_data['lead'][eb] += results_el['details']['lead'][res_bin][ab]['data']
                    ffs    ['lead'][eb] += results_el['details']['lead'][res_bin][ab]['ff']
                ana_bins_subl = [x for x in results_el['details']['subl'][res_bin].keys() if isinstance(x, tuple ) ]
                for ab in ana_bins_subl :
                    sb_data['subl'][eb] += results_el['details']['subl'][res_bin][ab]['data']
                    ffs    ['subl'][eb] += results_el['details']['subl'][res_bin][ab]['ff']

            print 'ADD 10% uncertainty to fake factors!'
            ffs['lead'][eb] += ufloat( 0.0, ffs['lead'][eb].n*0.1 )
            ffs['subl'][eb] += ufloat( 0.0, ffs['subl'][eb].n*0.1 )

            combined_fake[eb] = {}
            ele_pred_nom_lead = ffs['lead'][eb].n * ( sb_data['lead'][eb] - jet_sum['lead'][eb]['JetFake']['sum'] ) 
            ele_pred_nom_subl = ffs['subl'][eb].n * ( sb_data['subl'][eb] - jet_sum['subl'][eb]['JetFake']['sum'] )
            ele_pred_nom = ele_pred_nom_lead + ele_pred_nom_subl
            for syst in all_systs :

                # in channel combinations
                # only data statistics are
                # uncorrelated
                if syst == 'statData' :
                    ele_pred_lead = ufloat( ffs['lead'][eb].n, 0.0 ) * ( sb_data['lead'][eb] - jet_sum['lead'][eb][syst]['sum'] ) 
                    ele_pred_subl = ufloat( ffs['subl'][eb].n, 0.0 ) * ( sb_data['subl'][eb] - jet_sum['subl'][eb][syst]['sum'] )
                    ele_pred_tot = ele_pred_lead + ele_pred_subl
                    combined_fake[eb][syst] = jet_sum['nom'][eb][syst]['sum'] + ele_pred_tot
                else :
                    ele_jet_pred = ufloat( ffs['lead'][eb].n, 0.0 ) * jet_sum['lead'][eb][syst]['sum'] + ufloat( ffs['subl'][eb].n, 0.0 ) * jet_sum['subl'][eb][syst]['sum']
                    jet_comb = ufloat( jet_sum['nom'][eb][syst]['sum'].n - ele_jet_pred.n,  math.fabs(jet_sum['nom'][eb][syst]['sum'].s - ele_jet_pred.s ) ) 
                    ele_data = ffs['lead'][eb] * sb_data['lead'][eb] + ffs['subl'][eb]*sb_data['subl'][eb]
                    ele_data = ufloat( ele_data.n, 0.0 ) # no data uncert

                    combined_fake[eb][syst] = jet_comb + ele_data

            combined_fake[eb]['EleFakeFF'] = ufloat( jet_sum['nom'][eb]['JetFake']['sum'].n, 0.0 ) + ffs['lead'][eb]*(ufloat( sb_data['lead'][eb].n, 0.0 )  - ufloat(jet_sum['lead'][eb]['JetFake']['sum'].n, 0.0) ) + ffs['subl'][eb]*(ufloat( sb_data['subl'][eb].n, 0.0 )  - ufloat(jet_sum['subl'][eb]['JetFake']['sum'].n, 0.0) )

            print combined_fake[eb]

        bin_correlations_with_el = {'statTempTight' : False, 
                                    'crossCorr' : True,
                                    'systBkg' : True,
                                    'fakefake' : False, 
                                    'systTemp' : False, 
                                    'statTempLoose' : False, 
                                    'statData' : False,
                                    'EleFakeFF' : False}


        bin_combined_fake = {}
        for syst, isCorr in bin_correlations_with_el.iteritems() :
            bin_combined_fake[syst] = ufloat(0,0)

            for reg in combined_fake.keys() :

                if isCorr :
                    bin_combined_fake[syst] = ufloat( bin_combined_fake[syst].n + combined_fake[reg][syst].n, bin_combined_fake[syst].s + combined_fake[reg][syst].s )
                else:
                    bin_combined_fake[syst] = bin_combined_fake[syst] + combined_fake[reg][syst]

        summed_el['CombStat'] = bin_combined_fake['statData']
        summed_el['CombEleFakeFF'] = bin_combined_fake['EleFakeFF']
        
        summed_el['CombJetCorr'] = ufloat( bin_combined_fake['statData'].n, 0.0 )
        for syst, val in bin_combined_fake.iteritems() :
            if syst == 'statData' or syst == 'EleFakeFF' :
                continue

            summed_el['CombJetCorr'] += ufloat( 0.0, bin_combined_fake[syst].s )

    if zgg :
        return make_zgg_combination(results_final, jet_sum_mu, jet_sum_el, summed_mu, summed_el, pt_bins, eta_bins, outputDir=outputDir)
    else :
        return make_wgg_combination(results_final, jet_sum_mu, jet_sum_el, summed_mu, summed_el, pt_bins, eta_bins, outputDir=outputDir)

def make_wgg_combination( results_final, jet_sum_mu, jet_sum_el,summed_mu, summed_el, pt_bins, eta_bins, outputDir=None ) :

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
    print 'EleFake'
    print summed_el['EleFake']
    print 'JetFake'
    print summed_el['JetFake']

    summed_mu['ZggSyst'] = make_uncert_compliment( summed_mu['Zgg'], summed_mu['ZggStat'], isCorr=True )
    summed_el['ZggSyst'] = make_uncert_compliment( summed_el['Zgg'], summed_el['ZggStat'], isCorr=True )

    bkg_el = {}
    bkg_mu = {}
    bkg_mu['statData'] = summed_mu['JetFakeStat']['sum'] + ufloat( summed_mu['Zgg']['sum'].n, 0.0 )
    bkg_mu['ZggStat'] = ufloat( summed_mu['JetFakeStat']['sum'].n, 0.0) +  summed_mu['ZggStat']['sum']
    bkg_mu['ZggSyst'] = ufloat( summed_mu['JetFakeStat']['sum'].n, 0.0) +  summed_mu['ZggSyst']['sum']
    bkg_mu['lumi']    = ufloat( summed_mu['JetFakeStat']['sum'].n, 0.0) +  ufloat( summed_mu['Zgg']['sum'].n, summed_mu['Zgg']['sum'].n*0.026 )
    bkg_mu['JetFakeSyst'] = summed_mu['JetFakeSyst']['sum'] + ufloat(summed_mu['Zgg']['sum'].n, 0.0 )

    bkg_el['statData'] = summed_el['CombStat'] + ufloat( summed_el['Zgg']['sum'].n, 0.0 )
    bkg_el['JetFakeSyst'] = summed_el['CombJetCorr'] + ufloat( summed_el['Zgg']['sum'].n, 0.0 )
    bkg_el['EleFakeSyst'] = summed_el['CombEleFakeFF'] + ufloat( summed_el['Zgg']['sum'].n, 0.0 )
    bkg_el['ZggStat'] = ufloat(summed_el['CombStat'].n, 0.0) + summed_el['ZggStat']['sum']
    bkg_el['ZggSyst'] = ufloat(summed_el['CombStat'].n, 0.0) + summed_el['ZggSyst']['sum']
    bkg_el['lumi']    = ufloat( summed_el['CombStat'].n, 0.0) +  ufloat( summed_el['Zgg']['sum'].n, summed_el['Zgg']['sum'].n*0.026 )

    print 'bkg_mu'
    print bkg_mu
    print 'bkg_el'
    print bkg_el

    lumi = ufloat( 19.4, 19.4*0.026 )

    exp_mu = bkg_mu['statData'] + summed_mu['Wgg']['sum']
    exp_el = bkg_el['statData'] + summed_el['Wgg']['sum']
    xs_mu_sig =  (ufloat( exp_mu.n, math.sqrt(exp_mu.n) ) - bkg_mu['statData'])/ ( comb_acceptance['muon']['stat'] * lumi )
    xs_el_sig =  (ufloat(exp_el.n, math.sqrt(exp_el.n) ) - bkg_el['statData'] )/ ( comb_acceptance['electron']['stat'] * lumi )
    xs_mu = {}
    xs_el = {}

    print 'data mu'
    print summed_mu['Data']['sum']
    print 'data el'
    print summed_el['Data']['sum']



    xs_mu['statData']    = ( summed_mu['Data']['sum'] - bkg_mu['statData'] )                            / ( ufloat( comb_acceptance['muon']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_mu['ZggStat']     = ( ufloat(summed_mu['Data']['sum'].n,0.0) - bkg_mu['ZggStat'])                / ( ufloat( comb_acceptance['muon']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_mu['ZggSyst']     = ( ufloat(summed_mu['Data']['sum'].n,0.0) - bkg_mu['ZggSyst'])                / ( ufloat( comb_acceptance['muon']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_mu['JetFakeSyst'] = ( ufloat(summed_mu['Data']['sum'].n,0.0) - bkg_mu['JetFakeSyst'])            / ( ufloat( comb_acceptance['muon']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_mu['lumi']        = ( ufloat(summed_mu['Data']['sum'].n,0.0) - bkg_mu['lumi'])                   / ( ufloat( comb_acceptance['muon']['stat'].n, 0.0)*lumi)
    xs_mu['AccStat']     = ( ufloat(summed_mu['Data']['sum'].n,0.0) - ufloat(bkg_mu['statData'].n,0.0)) / ( comb_acceptance['muon']['stat']*ufloat(lumi.n, 0.0))
    xs_mu['AccChannel']  = ( ufloat(summed_mu['Data']['sum'].n,0.0) - ufloat(bkg_mu['statData'].n,0.0)) / ( comb_acceptance['muon']['Channel']*ufloat(lumi.n, 0.0))
    xs_mu['AccPhoton']  = ( ufloat(summed_mu['Data']['sum'].n,0.0) - ufloat(bkg_mu['statData'].n,0.0))  / ( comb_acceptance['muon']['Photon']*ufloat(lumi.n, 0.0))
    xs_mu['AccTheory']  = ( ufloat(summed_mu['Data']['sum'].n,0.0) - ufloat(bkg_mu['statData'].n,0.0))  / ( comb_acceptance['muon']['Theory']*ufloat(lumi.n, 0.0))
    xs_mu['EleFakeSyst']  = ufloat( xs_mu['statData'].n, 0.0 )

    xs_el['statData']    = ( summed_el['Data']['sum'] - bkg_el['statData'] )                            / ( ufloat( comb_acceptance['electron']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_el['ZggStat']     = ( ufloat(summed_el['Data']['sum'].n,0.0) - bkg_el['ZggStat'])                / ( ufloat( comb_acceptance['electron']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_el['ZggSyst']     = ( ufloat(summed_el['Data']['sum'].n,0.0) - bkg_el['ZggSyst'])                / ( ufloat( comb_acceptance['electron']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_el['JetFakeSyst'] = ( ufloat(summed_el['Data']['sum'].n,0.0) - bkg_el['JetFakeSyst'])            / ( ufloat( comb_acceptance['electron']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_el['EleFakeSyst'] = ( ufloat(summed_el['Data']['sum'].n,0.0) - bkg_el['EleFakeSyst'])            / ( ufloat( comb_acceptance['electron']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_el['lumi']        = ( ufloat(summed_el['Data']['sum'].n,0.0) - bkg_el['lumi'])                   / ( ufloat( comb_acceptance['electron']['stat'].n, 0.0)*lumi)
    xs_el['AccStat']     = ( ufloat(summed_el['Data']['sum'].n,0.0) - ufloat(bkg_el['statData'].n,0.0)) / ( comb_acceptance['electron']['stat']*ufloat(lumi.n, 0.0))
    xs_el['AccChannel']  = ( ufloat(summed_el['Data']['sum'].n,0.0) - ufloat(bkg_el['statData'].n,0.0)) / ( comb_acceptance['electron']['Channel']*ufloat(lumi.n, 0.0))
    xs_el['AccPhoton']  = ( ufloat(summed_el['Data']['sum'].n,0.0) - ufloat(bkg_el['statData'].n,0.0))  / ( comb_acceptance['electron']['Photon']*ufloat(lumi.n, 0.0))
    xs_el['AccTheory']  = ( ufloat(summed_el['Data']['sum'].n,0.0) - ufloat(bkg_el['statData'].n,0.0))  / ( comb_acceptance['electron']['Theory']*ufloat(lumi.n, 0.0))

    print 'xs_mu'
    print xs_mu
    print 'xs_el'
    print xs_el

    print 'Muon, N Data = %d, N Sig = %f, n Bkg = %s '      %( summed_mu['Data']['sum'].n, summed_mu['Wgg']['sum'].n, bkg_mu )
    print 'Electron , N Data = %d, N Sig = %f, n Bkg = %s ' %( summed_el['Data']['sum'].n, summed_el['Wgg']['sum'].n, bkg_el )
    #print 'S/sigma(B), mu =  %f ' %( summed_mu['Wgg']['sum'].n / bkg_mu.s )
    #print 'S/sigma(B), el =  %f ' %( summed_el['Wgg']['sum'].n / bkg_el.s )
    print 'xs_mu_sig = %s, frac unc = %f' %( xs_mu_sig, xs_mu_sig.s/xs_mu_sig.n)
    print 'xs_el_sig = %s, frac unc = %f' %( xs_el_sig, xs_el_sig.s/xs_el_sig.n)

    comb_xs_mu = xs_mu['statData'] + ufloat( 0.0, xs_mu['ZggStat'].s ) + ufloat( 0.0, xs_mu['ZggSyst'].s ) + ufloat( 0.0, xs_mu['JetFakeSyst'].s ) + ufloat( 0.0, xs_mu['lumi'].s ) + ufloat( 0.0, xs_mu['AccStat'].s ) + ufloat( 0.0, xs_mu['AccChannel'].s ) + ufloat( 0.0, xs_mu['AccPhoton'].s ) + ufloat( 0.0, xs_mu['AccTheory'].s )
    comb_xs_el = xs_el['statData'] + ufloat( 0.0, xs_el['ZggStat'].s ) + ufloat( 0.0, xs_el['ZggSyst'].s ) + ufloat( 0.0, xs_el['JetFakeSyst'].s ) + ufloat( 0.0, xs_el['lumi'].s ) + ufloat( 0.0, xs_el['EleFakeSyst'].s ) + ufloat( 0.0, xs_el['AccStat'].s ) + ufloat( 0.0, xs_el['AccChannel'].s ) + ufloat( 0.0, xs_el['AccPhoton'].s ) + ufloat( 0.0, xs_el['AccTheory'].s )

    print 'Final xs_mu = %s' %comb_xs_mu
    print 'Final xs_el = %s' %comb_xs_el

    xs_mu['central_value'] = comb_xs_mu
    xs_el['central_value'] = comb_xs_el

    ch_correlations  = {'statData'    : False, 
                        'JetFakeSyst' : True, 
                        'ZggStat'     : False, 
                        'ZggSyst'     : True, 
                        'lumi'        : True,
                        'AccStat'     : False,
                        'AccChannel'  : False,
                        'AccPhoton'   : True,
                        'AccTheory'   : True,
                       }
    
    extra_systs = {'EleFakeSyst' :xs_el['EleFakeSyst'] }

    xs_calc = blue.Calculator()
    meas_values = [comb_xs_mu.n, comb_xs_el.n]
    xs_calc.SetMeasurementValues( meas_values )

    # make BLUE calculators for each separate uncertainty
    calc_indiv = {}
    for syst in ch_correlations.keys() :
        calc_indiv[syst] = blue.Calculator()
        calc_indiv[syst].SetMeasurementValues( meas_values )


    n_ch = 2
    for syst, is_corr in ch_correlations.iteritems() :

        matrix  = []
        for i in range( 0, n_ch ) :
            list_i = [0]*n_ch
            for j in range( 0, n_ch ) :
                entry  = xs_mu[syst].s*xs_el[syst].s

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

    errsq_extra = 0.0
    for syst, val in extra_systs.iteritems() :
        errsq_extra += ( val.s/val.n ) * ( val.s/val.n )
    combined_error = math.sqrt( combined_error*combined_error +  errsq_extra*combined_value*combined_value )

    comb_results = {}
    comb_results['combined'] = ufloat( combined_value, combined_error )
    comb_results['isCorr'] = {}
    comb_results['systs'] = {}

    for unc, icalc in calc_indiv.iteritems() :
        print unc

        comb_results['isCorr'][unc] = ch_correlations[unc]

        value = icalc.CalculateCombinedValue()
        uncert= icalc.CalculateCombinedUncertainty()

        comb_results['systs'][unc] = ufloat( value, uncert )

    for syst in extra_systs.keys() :
        comb_results['isCorr'][syst] = False

    for syst, val in extra_systs.iteritems() :
        comb_results['systs'][syst] = ufloat( combined_value, (val.s/val.n)*combined_value )


    print 'Combined xs = %s' %( ufloat( combined_value, combined_error ) )
    print comb_results

    output_results = {}
    output_results['channels'] = {'muon' : {}, 'electron' : {} }

    output_results['channels']['muon']['JetSum'] = jet_sum_mu
    output_results['channels']['electron']['JetSum'] = jet_sum_el

    output_results['channels']['muon']['BkgSum'] = summed_mu
    output_results['channels']['electron']['BkgSum'] = summed_el

    output_results['channels']['muon']['CrossSection'] = xs_mu
    output_results['channels']['electron']['CrossSection'] = xs_el

    output_results['combination'] = comb_results

    if outputDir is not None :
        fname = '%s/%s' %( outputDir, 'cross_section_details.pickle' )
        print 'write %s' %fname
        outfile = open( fname, 'w' )
        pickle.dump( output_results, outfile )
        outfile.close()

    return output_results

def make_zgg_combination( results_final, jet_sum_mu, jet_sum_el,summed_mu, summed_el, pt_bins, eta_bins, outputDir=None ) :

    summed_mu['Zgg']  = get_summed_sample( results_final['muon'],  'Zgg' , pt_bins, eta_bins, isCorr=True )
    summed_mu['Data'] = get_summed_sample( results_final['muon'],  'Data', pt_bins, eta_bins, isCorr=False )

    summed_el['Zgg']     = get_summed_sample( results_final['electron'],  'Zgg'    , pt_bins, eta_bins, isCorr=True )
    summed_el['Data']    = get_summed_sample( results_final['electron'],  'Data'   , pt_bins, eta_bins, isCorr=False )

    bkg_el = {}
    bkg_mu = {}
    bkg_mu['statData']    = summed_mu['JetFakeStat']['sum'] 
    bkg_mu['JetFakeSyst'] = summed_mu['JetFakeSyst']['sum'] 

    bkg_el['statData']    = summed_el['JetFakeStat']['sum'] 
    bkg_el['JetFakeSyst'] = summed_el['JetFakeSyst']['sum'] 

    lumi = ufloat( 19.4, 19.4*0.026 )

    exp_mu = bkg_mu['statData'] + summed_mu['Zgg']['sum']
    exp_el = bkg_el['statData'] + summed_el['Zgg']['sum']

    xs_mu_sig =  (ufloat( exp_mu.n, math.sqrt(exp_mu.n) ) - bkg_mu['statData'])/ ( comb_acceptance_zgg['muon']['stat'] * lumi )
    xs_el_sig =  (ufloat(exp_el.n, math.sqrt(exp_el.n) ) - bkg_el['statData'] )/ ( comb_acceptance_zgg['electron']['stat'] * lumi )
    xs_mu = {}
    xs_el = {}

    xs_mu['statData']    = ( summed_mu['Data']['sum'] - bkg_mu['statData'] )                            / ( ufloat( comb_acceptance_zgg['muon']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_mu['JetFakeSyst'] = ( ufloat(summed_mu['Data']['sum'].n,0.0) - bkg_mu['JetFakeSyst'])            / ( ufloat( comb_acceptance_zgg['muon']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_mu['lumi']        = ( ufloat(summed_mu['Data']['sum'].n,0.0) - ufloat(bkg_mu['statData'].n,0.0)) / ( ufloat( comb_acceptance_zgg['muon']['stat'].n, 0.0)*lumi)
    xs_mu['AccStat']     = ( ufloat(summed_mu['Data']['sum'].n,0.0) - ufloat(bkg_mu['statData'].n,0.0)) / ( comb_acceptance_zgg['muon']['stat']*ufloat(lumi.n, 0.0))
    xs_mu['AccChannel']  = ( ufloat(summed_mu['Data']['sum'].n,0.0) - ufloat(bkg_mu['statData'].n,0.0)) / ( comb_acceptance_zgg['muon']['Channel']*ufloat(lumi.n, 0.0))
    xs_mu['AccPhoton']   = ( ufloat(summed_mu['Data']['sum'].n,0.0) - ufloat(bkg_mu['statData'].n,0.0))  / ( comb_acceptance_zgg['muon']['Photon']*ufloat(lumi.n, 0.0))
    xs_mu['AccTheory']   = ( ufloat(summed_mu['Data']['sum'].n,0.0) - ufloat(bkg_mu['statData'].n,0.0))  / ( comb_acceptance_zgg['muon']['Theory']*ufloat(lumi.n, 0.0))

    xs_el['statData']    = ( summed_el['Data']['sum'] - bkg_el['statData'] )                     / ( ufloat( comb_acceptance_zgg['electron']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_el['JetFakeSyst'] = ( ufloat(summed_el['Data']['sum'].n,0.0) - bkg_el['JetFakeSyst'])     / ( ufloat( comb_acceptance_zgg['electron']['stat'].n, 0.0)*ufloat(lumi.n, 0.0) )
    xs_el['lumi']        = ( ufloat(summed_el['Data']['sum'].n,0.0) - ufloat(bkg_el['statData'].n,0.0)) / ( ufloat( comb_acceptance_zgg['electron']['stat'].n, 0.0)*lumi)
    xs_el['AccStat']     = ( ufloat(summed_el['Data']['sum'].n,0.0) - ufloat(bkg_el['statData'].n,0.0)) / ( comb_acceptance_zgg['electron']['stat']*ufloat(lumi.n, 0.0))
    xs_el['AccChannel']  = ( ufloat(summed_el['Data']['sum'].n,0.0) - ufloat(bkg_el['statData'].n,0.0)) / ( comb_acceptance_zgg['electron']['Channel']*ufloat(lumi.n, 0.0))
    xs_el['AccPhoton']   = ( ufloat(summed_el['Data']['sum'].n,0.0) - ufloat(bkg_el['statData'].n,0.0))  / ( comb_acceptance_zgg['electron']['Photon']*ufloat(lumi.n, 0.0))
    xs_el['AccTheory']   = ( ufloat(summed_el['Data']['sum'].n,0.0) - ufloat(bkg_el['statData'].n,0.0))  / ( comb_acceptance_zgg['electron']['Theory']*ufloat(lumi.n, 0.0))

    print 'xs_mu'
    print xs_mu
    print 'xs_el'
    print xs_el

    print 'Muon, N Data = %d, N Sig = %f, n Bkg = %s '      %( summed_mu['Data']['sum'].n, summed_mu['Zgg']['sum'].n, bkg_mu )
    print 'Electron , N Data = %d, N Sig = %f, n Bkg = %s ' %( summed_el['Data']['sum'].n, summed_el['Zgg']['sum'].n, bkg_el )
    #print 'S/sigma(B), mu =  %f ' %( summed_mu['Wgg']['sum'].n / bkg_mu.s )
    #print 'S/sigma(B), el =  %f ' %( summed_el['Wgg']['sum'].n / bkg_el.s )
    print 'xs_mu_sig = %s, frac unc = %f' %( xs_mu_sig, xs_mu_sig.s/xs_mu_sig.n)
    print 'xs_el_sig = %s, frac unc = %f' %( xs_el_sig, xs_el_sig.s/xs_el_sig.n)

    comb_xs_mu = xs_mu['statData'] + ufloat( 0.0, xs_mu['JetFakeSyst'].s ) + ufloat( 0.0, xs_mu['lumi'].s ) + ufloat( 0.0, xs_mu['AccStat'].s ) + ufloat( 0.0, xs_mu['AccChannel'].s ) + ufloat( 0.0, xs_mu['AccPhoton'].s ) + ufloat( 0.0, xs_mu['AccTheory'].s )
    comb_xs_el = xs_el['statData'] + ufloat( 0.0, xs_el['JetFakeSyst'].s ) + ufloat( 0.0, xs_el['lumi'].s ) + ufloat( 0.0, xs_el['AccStat'].s ) + ufloat( 0.0, xs_el['AccChannel'].s ) + ufloat( 0.0, xs_el['AccPhoton'].s ) + ufloat( 0.0, xs_el['AccTheory'].s )

    print 'Final xs_mu = %s' %comb_xs_mu
    print 'Final xs_el = %s' %comb_xs_el

    xs_mu['central_value'] = comb_xs_mu
    xs_el['central_value'] = comb_xs_el

    ch_correlations  = {'statData'    : False, 
                        'JetFakeSyst' : True, 
                        'lumi'        : True,
                        'AccStat'     : False,
                        'AccChannel'  : False,
                        'AccPhoton'   : True,
                        'AccTheory'   : True,
                       }
    
    extra_systs = { }

    xs_calc = blue.Calculator()
    meas_values = [comb_xs_mu.n, comb_xs_el.n]
    xs_calc.SetMeasurementValues( meas_values )

    # make BLUE calculators for each separate uncertainty
    calc_indiv = {}
    for syst in ch_correlations.keys() :
        calc_indiv[syst] = blue.Calculator()
        calc_indiv[syst].SetMeasurementValues( meas_values )


    n_ch = 2
    for syst, is_corr in ch_correlations.iteritems() :

        matrix  = []
        for i in range( 0, n_ch ) :
            list_i = [0]*n_ch
            for j in range( 0, n_ch ) :
                entry  = xs_mu[syst].s*xs_el[syst].s

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

    errsq_extra = 0.0
    for syst, val in extra_systs.iteritems() :
        errsq_extra += ( val.s/val.n ) * ( val.s/val.n )
    combined_error = math.sqrt( combined_error*combined_error +  errsq_extra*combined_value*combined_value )

    comb_results = {}
    comb_results['combined'] = ufloat( combined_value, combined_error )
    comb_results['isCorr'] = {}
    comb_results['systs'] = {}

    for unc, icalc in calc_indiv.iteritems() :
        print unc

        comb_results['isCorr'][unc] = ch_correlations[unc]

        value = icalc.CalculateCombinedValue()
        uncert= icalc.CalculateCombinedUncertainty()

        comb_results['systs'][unc] = ufloat( value, uncert )

    for syst in extra_systs.keys() :
        comb_results['isCorr'][syst] = False

    for syst, val in extra_systs.iteritems() :
        comb_results['systs'][syst] = ufloat( combined_value, (val.s/val.n)*combined_value )


    print 'Combined xs = %s' %( ufloat( combined_value, combined_error ) )
    print comb_results

    output_results = {}
    output_results['channels'] = {'muon' : {}, 'electron' : {} }

    output_results['channels']['muon']['JetSum'] = jet_sum_mu
    output_results['channels']['electron']['JetSum'] = jet_sum_el

    output_results['channels']['muon']['BkgSum'] = summed_mu
    output_results['channels']['electron']['BkgSum'] = summed_el

    output_results['channels']['muon']['CrossSection'] = xs_mu
    output_results['channels']['electron']['CrossSection'] = xs_el

    output_results['combination'] = comb_results

    if outputDir is not None :
        fname = '%s/%s' %( outputDir, 'cross_section_details.pickle' )
        print 'write %s' %fname
        outfile = open( fname, 'w' )
        pickle.dump( output_results, outfile )
        outfile.close()

    return output_results 

def collect_jet_systs( jet_sum, all_systs, bin_correlations ) :

    jet_tot = None

    jet_tot_data = None

    jet_tot_binuncorr = None

    jet_tot_bincorr = None

    jet_tot_syst = None

    summed = {}

    for idx, syst in enumerate( all_systs ) :

        summed[syst] = {'sum' : jet_sum['sum'][syst] }

        if idx == 0 :
            jet_tot = jet_sum['sum'][syst] 
        else :
            jet_tot += ufloat( 0.0, jet_sum['sum'][syst].s )

        if bin_correlations[syst] :
            if jet_tot_bincorr is None :
                jet_tot_bincorr = jet_sum['sum'][syst]
            else : 
                jet_tot_bincorr += ufloat( 0.0, jet_sum['sum'][syst].s )
        else :
            if jet_tot_binuncorr is None :
                jet_tot_binuncorr = jet_sum['sum'][syst]
            else : 
                jet_tot_binuncorr += ufloat( 0.0, jet_sum['sum'][syst].s )

        if syst == 'statData' :
            jet_tot_data = jet_sum['sum'][syst]
        else :
            if jet_tot_syst is None :
                jet_tot_syst = jet_sum['sum'][syst]
            else :
                jet_tot_syst += ufloat( 0.0, jet_sum['sum'][syst].s )
    

    summed['JetFake']          = { 'sum' : jet_tot }
    summed['JetFakeStat']      = { 'sum' : jet_tot_data }

    summed['JetFakeSyst']      = { 'sum' : jet_tot_syst }

    summed['JetFakeBinCorr']   = { 'sum' : jet_tot_bincorr }

    summed['JetFakeBinUncorr'] = { 'sum' : jet_tot_binuncorr }

    return summed

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

def get_dic_from_pickle( filename ) :

    ofile= open( filename )
    results = pickle.load( ofile)
    ofile.close()

    return results

def collect_match_results_from_pickle( baseDir, files ) :

    results = {}
    for fname, matchdic in files :
        region = ( matchdic['reg1'], matchdic['reg2'] )
        ofile = open( '%s/%s' %( baseDir , fname ) )
        results[region] = pickle.load( ofile )
        ofile.close()

    return results

def get_matching_regex( full_list, match ) :
    
    matches = []

    for obj in full_list :
        res = re.match( match, obj )

        if res is not None :
            matches.append( ( obj, res.groupdict() ) )

    return matches







main()
