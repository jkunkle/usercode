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

## FOR EB_EB+EB_EE+EE_EB, > 40
#acceptances = { 'electron' : {
#                              ('15', '25')  : ufloat( 1.0, 0.0) , 
#                              ('25', '40')  : ufloat( 1.0, 0.0) ,
#                              ('40', '70')  : ufloat( 0.1596, 0.0280) ,
#                              ('70', 'max') : ufloat( 0.2023, 0.0358 ) ,
#                             },
#                'muon'    : { 
#                              ('15', '25')  : ufloat( 1.0, 0.0 ) , 
#                              ('25', '40')  : ufloat( 1.0, 0.0 ) ,
#                              ('40', '70')  : ufloat( 0.2645, 0.0074 ) ,
#                              ('70', 'max') : ufloat( 0.2848, 0.0082 ) ,
#                             },
#}

acc_egg = ufloat( 0.1725,0.0)
acc_mgg = ufloat( 0.2669,0.0)

stat_egg           = ufloat( 0.0, acc_egg.n*0.0278 )
syst_egg_trig      = ufloat( 0.0, acc_egg.n*0.0046 )
syst_egg_ele       = ufloat( 0.0, acc_egg.n*0.0012 ) 
syst_egg_phot      = ufloat( 0.0, acc_egg.n*0.0206 )
syst_egg_eveto     = ufloat( 0.0, acc_egg.n*0.0304 )
syst_egg_pdf       = ufloat( 0.0, acc_egg.n*0.0125 )
syst_egg_pu        = ufloat( 0.0, acc_egg.n*0.0049 )
#syst_egg_scale_eg  = ufloat( 0.0, acc_egg.n*0.0209 )
syst_egg_scale_eg  = ufloat( 0.0, acc_egg.n*0.0184 )
#syst_egg_scale_met = ufloat( 0.0, acc_egg.n*0.0165 )
syst_egg_scale_met = ufloat( 0.0, acc_egg.n*0.0152 )
syst_egg_renorm_fact    = ufloat( 0.0, acc_egg.n*0.0078 )
#syst_egg_fact      = ufloat( 0.0, acc_egg.n*0.0008 )

stat_mgg           = ufloat( 0.0, acc_mgg.n*0.0240 )
syst_mgg_trig      = ufloat( 0.0, acc_mgg.n*0.0026 )
syst_mgg_phot      = ufloat( 0.0, acc_mgg.n*0.0204 )
syst_mgg_muonidiso    = ufloat( 0.0, acc_mgg.n*0.0027 )
#syst_mgg_pdf       = ufloat( 0.0, acc_mgg.n*0.0164 )
syst_mgg_pdf       = ufloat( 0.0, acc_mgg.n*0.0145 )
syst_mgg_pu        = ufloat( 0.0, acc_mgg.n*0.0017 )
#syst_mgg_scale_eg  = ufloat( 0.0, acc_mgg.n*0.0217 )
syst_mgg_scale_eg  = ufloat( 0.0, acc_mgg.n*0.0210 )
#syst_mgg_scale_met = ufloat( 0.0, acc_mgg.n*0.0176 )
syst_mgg_scale_met = ufloat( 0.0, acc_mgg.n*0.0139 )
#syst_mgg_scale_mu  = ufloat( 0.0, acc_mgg.n*0.0026 )
syst_mgg_scale_mu  = ufloat( 0.0, acc_mgg.n*0.0019 )
syst_mgg_renorm_fact    = ufloat( 0.0, acc_mgg.n*0.0077 )
#syst_mgg_fact      = ufloat( 0.0, acc_mgg.n*0.0006 )

acc_eegg = ufloat( 0.2249, 0.0 )
acc_mmgg = ufloat( 0.2911, 0.0 )

stat_eegg           = ufloat( 0.0, acc_eegg.n*0.0325 )
syst_eegg_trig      = ufloat( 0.0, acc_eegg.n*0.0133 )
syst_eegg_ele       = ufloat( 0.0, acc_eegg.n*0.0371 )
syst_eegg_phot      = ufloat( 0.0, acc_eegg.n*0.0278 )
syst_eegg_eveto     = ufloat( 0.0, acc_eegg.n*0.0076 )
#syst_eegg_pdf       = ufloat( 0.0, acc_eegg.n*0.0159 )
syst_eegg_pdf       = ufloat( 0.0, acc_eegg.n*0.0105 )
syst_eegg_pu        = ufloat( 0.0, acc_eegg.n*0.0131 )
syst_eegg_scale_eg  = ufloat( 0.0, acc_eegg.n*0.0252 )
syst_eegg_renorm_fact    = ufloat( 0.0, acc_eegg.n*0.0055 )
#syst_eegg_fact      = ufloat( 0.0, acc_eegg.n*0.0024 )

stat_mmgg           = ufloat( 0.0, acc_mmgg.n*0.0289 )
syst_mmgg_trig      = ufloat( 0.0, acc_mmgg.n*0.0120 )
syst_mmgg_phot      = ufloat( 0.0, acc_mmgg.n*0.0282 )
syst_mmgg_eveto     = ufloat( 0.0, acc_mmgg.n*0.0076 )
syst_mmgg_muonidiso    = ufloat( 0.0, acc_mmgg.n*0.0046 )
#syst_mmgg_muoniso   = ufloat( 0.0, acc_mmgg.n*0.0021 )
syst_mmgg_pdf       = ufloat( 0.0, acc_mmgg.n*0.0111 )
syst_mmgg_pu        = ufloat( 0.0, acc_mmgg.n*0.0043 )
syst_mmgg_scale_eg  = ufloat( 0.0, acc_mmgg.n*0.0262 )
syst_mmgg_scale_mu  = ufloat( 0.0, acc_mmgg.n*0.0160 )
syst_mmgg_renorm_fact    = ufloat( 0.0, acc_mmgg.n*0.0068 )
#syst_mmgg_fact      = ufloat( 0.0, acc_mmgg.n*0.0048 )

comb_egg_stat      = acc_egg + stat_egg
comb_egg_leptonID  = acc_egg + syst_egg_trig + syst_egg_ele 
comb_egg_photonID  = acc_egg + syst_egg_phot 
comb_egg_photonEV  = acc_egg + syst_egg_eveto
comb_egg_egscale   = acc_egg + syst_egg_scale_eg
comb_egg_muscale   = acc_egg
comb_egg_met       = acc_egg + syst_egg_scale_met
comb_egg_pu        = acc_egg + syst_egg_pu
comb_egg_theory   = acc_egg + syst_egg_pdf + syst_egg_renorm_fact

comb_mgg_stat     = acc_mgg + stat_mgg
comb_mgg_leptonID = acc_mgg + syst_mgg_trig + syst_mgg_muonidiso
comb_mgg_photonID = acc_mgg + syst_mgg_phot
comb_mgg_photonEV = acc_mgg 
comb_mgg_egscale  = acc_mgg + syst_mgg_scale_eg
comb_mgg_muscale  = acc_mgg + syst_mgg_scale_mu
comb_mgg_met      = acc_mgg + syst_mgg_scale_met
comb_mgg_pu       = acc_mgg + syst_mgg_pu
comb_mgg_theory   = acc_mgg + syst_mgg_pdf + syst_mgg_renorm_fact

comb_eegg_stat     = acc_eegg + stat_eegg
comb_eegg_leptonID = acc_eegg + syst_eegg_trig + syst_eegg_ele
comb_eegg_photonID = acc_eegg + syst_eegg_phot + syst_eegg_eveto
comb_eegg_egscale  = acc_eegg + syst_eegg_scale_eg
comb_eegg_muscale  = acc_eegg
comb_eegg_pu       = acc_eegg + syst_eegg_pu
comb_eegg_theory   = acc_eegg + syst_eegg_pdf + syst_eegg_renorm_fact

comb_mmgg_stat     = acc_mmgg + stat_mmgg
comb_mmgg_leptonID = acc_mmgg + syst_mmgg_trig + syst_mmgg_muonidiso
comb_mmgg_photonID = acc_mmgg + syst_mmgg_phot + syst_mmgg_eveto
comb_mmgg_egscale  = acc_mmgg + syst_mmgg_scale_eg
comb_mmgg_muscale  = acc_mmgg + syst_mmgg_scale_mu
comb_mmgg_pu       = acc_mmgg + syst_mmgg_pu
comb_mmgg_theory   = acc_mmgg + syst_mmgg_pdf + syst_mmgg_renorm_fact

comb_acceptance =     { 'muon' : {
                                    'stat'     : comb_mgg_stat, 
                                    'LeptonID' : comb_mgg_leptonID,
                                    'PhotonID' : comb_mgg_photonID, 
                                    'PhotonEV' : comb_mgg_photonEV, 
                                    'EGScale'  : comb_mgg_egscale, 
                                    'MuScale'  : comb_mgg_muscale, 
                                    'MET'      : comb_mgg_met, 
                                    'Pileup'   : comb_mgg_pu, 
                                    'Theory'   : comb_mgg_theory, 
                                 },
                       'electron' : {
                                    'stat'     : comb_egg_stat,
                                    'LeptonID' : comb_egg_leptonID,
                                    'PhotonID' : comb_egg_photonID, 
                                    'PhotonEV' : comb_egg_photonEV, 
                                    'EGScale'  : comb_egg_egscale, 
                                    'MuScale'  : comb_egg_muscale, 
                                    'MET'      : comb_egg_met, 
                                    'Pileup'   : comb_egg_pu, 
                                    'Theory'   : comb_egg_theory, 
                                    }
                     }



comb_acceptance_zgg =  { 'muon' : {
                                    'stat'     : comb_mmgg_stat, 
                                    'LeptonID' : comb_mmgg_leptonID,
                                    'PhotonID' : comb_mmgg_photonID, 
                                    'EGScale'  : comb_mmgg_egscale, 
                                    'MuScale'  : comb_mmgg_muscale, 
                                    'Pileup'   : comb_mmgg_pu, 
                                    'Theory'   : comb_mmgg_theory, 
                                 },
                       'electron' : {
                                    'stat'     : comb_eegg_stat, 
                                    'LeptonID' : comb_eegg_leptonID,
                                    'PhotonID' : comb_eegg_photonID, 
                                    'EGScale'  : comb_eegg_egscale, 
                                    'MuScale'  : comb_eegg_muscale, 
                                    'Pileup'   : comb_eegg_pu, 
                                    'Theory'   : comb_eegg_theory, 
                                    }
                     }


def main() :

    #baseDirWgg  = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2015_10_13/'
    #plotDirWgg  = 'PlotsUnblindMCNDWithPhoWithCorrNoDiffUncNewOneBin'
    #finalDirWgg = 'FinalPlotsPlotsUnblindMCNDWithPhoWithCorrNoDiffUncNewOneBin'

    #baseDirZgg  = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2015_10_15/'
    #plotDirZgg  = 'PlotsUnblindZggNewOneBin'
    #finalDirZgg = 'FinalPlotsOneBin'

    baseDirWgg  = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlotsPSVTightMassOneBin_2015_12_01/'
    plotDirWgg  = 'PlotsUnblind'
    finalDirWgg = 'FinalPlotsOneBin'

    baseDirZgg  = '/afs/cern.ch/user/j/jkunkle/Plots/ZggPlotsOneBin_2015_12_01/'
    plotDirZgg  = 'PlotsUnblind'
    finalDirZgg = 'FinalPlotsOneBin'

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


    bin_correlations = { 
                        'crossCorr' : True,
                        'systBkg' : True,
                        'fakefake' : False, 
                        'systTemp' : False, 
                        'statTempLoose' : False, 
                        'statTempTight' : False, 
                        'statTempFF' : False, 
                        'statDataSB' : False,
                        'statDataSR' : False }

    jet_correlations = { 
                        'crossCorr' : True,
                        'systBkg' : True,
                        'fakefake' : False, 
                        'systTemp' : True, 
                        'statTemp1D' : True, 
                        'statTempFF' : True, 
                        }

    all_systs = ['statTempLoose', 'statTempTight', 'statTempFF', 'systTemp', 'systBkg', 'fakefake', 'crossCorr', 'statDataSB', 'statDataSR']
    systs_comb = ['statTemp1D', 'statTempFF', 'systTemp', 'systBkg', 'fakefake', 'crossCorr', 'statDataSB', 'statDataSR']

    jet_sum_el = get_simple_jet_bin_sums( results_jet['electron'], all_systs, eta_bins, pt_bins, bin_correlations )
    jet_sum_mu = get_simple_jet_bin_sums( results_jet['muon']    , all_systs, eta_bins, pt_bins, bin_correlations )

    summed_el = collect_jet_systs( jet_sum_el, all_systs)
    summed_mu = collect_jet_systs( jet_sum_mu, all_systs)

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
            # jet fake, invert lead SB
            jet_sum['lead'][eb] = collect_jet_systs( get_simple_jet_bin_sums( results_jet_lead, all_systs, [eb], pt_bins, bin_correlations ), all_systs)
            # jet fake, invert subl SB
            jet_sum['subl'][eb] = collect_jet_systs( get_simple_jet_bin_sums( results_jet_subl, all_systs, [eb], pt_bins, bin_correlations ), all_systs)
            # jet fake, ele SR
            jet_sum['nom' ][eb] = collect_jet_systs( get_simple_jet_bin_sums( results_jet['electron'], all_systs, [eb], pt_bins, bin_correlations ), all_systs)

            sb_data['lead'][eb] = ufloat(0,0)
            sb_data['subl'][eb] = ufloat(0,0)
            ffs['lead'][eb] = ufloat(0,0)
            ffs['subl'][eb] = ufloat(0,0)
            for ptmin, ptmax in pt_bins :
                res_bin = (eb[0],eb[1],ptmin,ptmax)
                # for this result bin, get the 
                # bins contained
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
            ele_is_neg = False
            # first determine if we need to 
            # resolve a negative estimate
            # with the fake factor uncertainty
            ele_sum  = ffs['lead'][eb]*(ufloat( sb_data['lead'][eb].n, 0.0 )  - ufloat(jet_sum['lead'][eb]['statDataSR']['sum'].n, 0.0) ) + ffs['subl'][eb]*(ufloat( sb_data['subl'][eb].n, 0.0 )  - ufloat(jet_sum['subl'][eb]['statDataSR']['sum'].n, 0.0) )
            if ele_sum.n <  0 :
                ele_is_neg = True
                ele_sum = ufloat( 0.0, ele_sum.s )
            combined_fake[eb]['EleFakeFF'] = {}
            combined_fake[eb]['EleFakeFF']['sum'] = ufloat( jet_sum['nom'][eb]['statDataSR']['sum'].n, 0.0 ) + ele_sum 
            combined_fake[eb]['EleFakeFF']['jet'] = ufloat( jet_sum['nom'][eb]['statDataSR']['sum'].n, 0.0 )
            combined_fake[eb]['EleFakeFF']['jetlead'] = ufloat( jet_sum['lead'][eb]['statDataSR']['sum'].n, 0.0 )
            combined_fake[eb]['EleFakeFF']['jetsubl'] = ufloat( jet_sum['subl'][eb]['statDataSR']['sum'].n, 0.0 )
            combined_fake[eb]['EleFakeFF']['datalead'] = ufloat( sb_data['lead'][eb].n, 0.0 )
            combined_fake[eb]['EleFakeFF']['datasubl'] = ufloat( sb_data['subl'][eb].n, 0.0 )
            combined_fake[eb]['EleFakeFF']['fflead'] = ffs['lead'][eb]
            combined_fake[eb]['EleFakeFF']['ffsubl'] = ffs['subl'][eb]
            combined_fake[eb]['EleFakeFF']['ele'] = ele_sum

            for syst in systs_comb :


                print 'Syst is ', syst

                # in channel combinations
                # only data statistics are
                # uncorrelated
                if syst == 'statDataSB' :
                    # the SR uncertainties from the 
                    # jet fakes in the ele fake sidebands
                    # are correlated to the data in the
                    # ele fake sidebands

                    # the data from the ele fake SB is combined
                    # correlated with the jet fake SR uncertainty
                    lead_sub_sr = ufloat( sb_data['lead'][eb].n - jet_sum['lead'][eb]['statDataSR']['sum'].n, sb_data['lead'][eb].s - jet_sum['lead'][eb]['statDataSR']['sum'].s )
                    subl_sub_sr = ufloat( sb_data['subl'][eb].n - jet_sum['subl'][eb]['statDataSR']['sum'].n, sb_data['subl'][eb].s - jet_sum['subl'][eb]['statDataSR']['sum'].s )

                    # the jet fake SB uncertainties are 
                    # independent of the data uncertainty 
                    # which is counted above
                    lead_sub_sb = ufloat( sb_data['lead'][eb].n, 0.0 ) - jet_sum['lead'][eb]['statDataSB']['sum']
                    subl_sub_sb = ufloat( sb_data['subl'][eb].n, 0.0 ) - jet_sum['subl'][eb]['statDataSB']['sum']

                    # now combine the two uncertainties in quadrature
                    lead_sub_sb = lead_sub_sb + ufloat( 0.0, lead_sub_sr.s )
                    subl_sub_sb = subl_sub_sb + ufloat( 0.0, subl_sub_sr.s )
                    
                    # now multiply by the fake factors
                    ele_pred_lead = ufloat( ffs['lead'][eb].n, 0.0 ) * (lead_sub_sb ) 
                    ele_pred_subl = ufloat( ffs['subl'][eb].n, 0.0 ) * (subl_sub_sb )
                    ele_pred_tot = ele_pred_lead + ele_pred_subl
                    print 'ElE PRED TOT BEFORE ', ele_pred_tot
                    ele_pred_tot = resolve_negatives( ele_pred_tot )
                    print 'ff lead = ', ffs['lead'][eb]
                    print 'ff subl = ', ffs['subl'][eb]
                    print 'data lead = ', sb_data['lead'][eb]
                    print 'data subl = ', sb_data['subl'][eb]
                    print 'jet lead = ', jet_sum['lead'][eb][syst]['sum']
                    print 'jet subl = ', jet_sum['subl'][eb][syst]['sum']
                    print 'ElE PRED TOT with ele SB ', ele_pred_tot
                    combined_fake[eb][syst] = {}
                    combined_fake[eb][syst]['sum'] = jet_sum['nom'][eb][syst]['sum'] + ele_pred_tot
                    combined_fake[eb][syst]['jetleadSR'] =  jet_sum['lead'][eb]['statDataSR']['sum']
                    combined_fake[eb][syst]['jetsublSR'] =  jet_sum['subl'][eb]['statDataSR']['sum']
                    combined_fake[eb][syst]['jetleadSB'] =  jet_sum['lead'][eb]['statDataSB']['sum']
                    combined_fake[eb][syst]['jetsublSB'] =  jet_sum['subl'][eb]['statDataSB']['sum']
                    combined_fake[eb][syst]['datalead'] =  sb_data['lead'][eb]
                    combined_fake[eb][syst]['datasubl'] =  sb_data['subl'][eb]
                    combined_fake[eb][syst]['fflead'] =  ufloat(ffs['lead'][eb].n, 0.0 )
                    combined_fake[eb][syst]['ffsubl'] =  ufloat(ffs['subl'][eb].n, 0.0 )
                    combined_fake[eb][syst]['jet'] = jet_sum['nom'][eb][syst]['sum']
                    combined_fake[eb][syst]['ele'] = ele_pred_tot

                elif syst == 'statDataSR' :
                    # SR data only comes from the jet fake
                    ele_pred_lead = ufloat( ffs['lead'][eb].n, 0.0 ) * ( ufloat(sb_data['lead'][eb].n, 0.0 ) - jet_sum['lead'][eb][syst]['sum'] ) 
                    ele_pred_subl = ufloat( ffs['subl'][eb].n, 0.0 ) * ( ufloat(sb_data['subl'][eb].n, 0.0 ) - jet_sum['subl'][eb][syst]['sum'] )
                    ele_pred_tot = ele_pred_lead + ele_pred_subl
                    ele_pred_tot = resolve_negatives( ele_pred_tot )
                    combined_fake[eb][syst] = {}
                    combined_fake[eb][syst]['sum'] = jet_sum['nom'][eb][syst]['sum'] + ele_pred_tot
                    combined_fake[eb][syst]['jet'] = jet_sum['nom'][eb][syst]['sum'] 
                    combined_fake[eb][syst]['ele'] = ele_pred_tot
                    combined_fake[eb][syst]['jetlead'] = ufloat( jet_sum['lead'][eb][syst]['sum'].n, 0.0 )
                    combined_fake[eb][syst]['jetsubl'] = ufloat( jet_sum['subl'][eb][syst]['sum'].n, 0.0 )
                    combined_fake[eb][syst]['datalead'] = ufloat( sb_data['lead'][eb].n, 0.0)
                    combined_fake[eb][syst]['datasubl'] = ufloat( sb_data['subl'][eb].n, 0.0)
                    combined_fake[eb][syst]['fflead'] = ufloat(ffs['lead'][eb].n, 0.0)
                    combined_fake[eb][syst]['ffsubl'] = ufloat(ffs['subl'][eb].n, 0.0)

                else :
                    iscorr = jet_correlations[syst]

                    # get jet fake contribution to prediction of electron fakes including jet background systematics 
                    ele_pred_jet_lead = ufloat( ffs['lead'][eb].n, 0.0 ) * jet_sum['lead'][eb][syst]['sum']
                    ele_pred_jet_subl = ufloat( ffs['subl'][eb].n, 0.0 ) * jet_sum['subl'][eb][syst]['sum']
                    if iscorr :
                        ele_pred_jet = ufloat( ele_pred_jet_lead.n + ele_pred_jet_subl.n, ele_pred_jet_lead.s + ele_pred_jet_subl.s )
                    else :
                        ele_pred_jet = ele_pred_jet_lead + ele_pred_jet_subl
                    #ele_pred_jet_lead = ufloat( ffs['lead'][eb].n, 0.0 ) * jet_sum['lead'][eb][syst]['sum']
                    #ele_pred_jet_subl = ufloat( ffs['subl'][eb].n, 0.0 ) * jet_sum['subl'][eb][syst]['sum']
                    #ele_pred_jet = ele_pred_jet_lead + ele_pred_jet_subl

                    print 'ele_pred_jet_lead', ele_pred_jet_lead
                    print 'ele_pred_jet_subl', ele_pred_jet_subl
                    print 'ele_pred_jet',ele_pred_jet
                    # combine jet fake in SR with jet fake components in ele SBs
                    # The jet fakes are subtracted in the SBs
                    # treat as fully correlated
                    if iscorr :
                        jet_comb = ufloat( jet_sum['nom'][eb][syst]['sum'].n - ele_pred_jet.n,  math.fabs(jet_sum['nom'][eb][syst]['sum'].s - ele_pred_jet.s ) ) 
                    else :
                        jet_comb = jet_sum['nom'][eb][syst]['sum'] - ele_pred_jet 

                    #jet_comb = jet_sum['nom'][eb][syst]['sum'] - ele_pred_jet
                    # SB data multiplied by fake factor
                    # do not include uncertainties here
                    ele_data = ffs['lead'][eb] * sb_data['lead'][eb] + ffs['subl'][eb]*sb_data['subl'][eb]
                    ele_data = ufloat( ele_data.n, 0.0 ) # no data uncert

                    # this is the jet fake plus electron fake
                    combined_fake[eb][syst] = {}
                    comb = jet_comb + ele_data
                    if ele_is_neg :
                        # set electron to zero , cv is jet only, with full uncertainty
                        comb = ufloat(jet_sum['nom'][eb][syst]['sum'].n, comb.s )

                    combined_fake[eb][syst]['sum']      = comb
                    combined_fake[eb][syst]['jet']      = jet_sum['nom'][eb][syst]['sum']
                    combined_fake[eb][syst]['jetlead']  = jet_sum['lead'][eb][syst]['sum']
                    combined_fake[eb][syst]['jetsubl']  = jet_sum['subl'][eb][syst]['sum']
                    combined_fake[eb][syst]['datalead'] = ufloat( sb_data['lead'][eb].n, 0.0)
                    combined_fake[eb][syst]['datasubl'] = ufloat( sb_data['subl'][eb].n, 0.0)
                    combined_fake[eb][syst]['fflead']   = ufloat(ffs['lead'][eb].n, 0.0)
                    combined_fake[eb][syst]['ffsubl']   = ufloat(ffs['subl'][eb].n, 0.0)


        bin_correlations_with_el = { 
                                    'crossCorr' : False,
                                    'systBkg' : True,
                                    'fakefake' : False, 
                                    'systTemp' : False, 
                                    'statTemp1D' : False, 
                                    'statTempFF' : False, 
                                    'statDataSB' : False,
                                    'statDataSR' : False,
                                    'EleFakeFF' : False}


        # combine across bins
        bin_combined_fake = {}
        for syst, isCorr in bin_correlations_with_el.iteritems() :
            bin_combined_fake[syst] = ufloat(0,0)

            for reg in combined_fake.keys() :

                if isCorr :
                    bin_combined_fake[syst] = ufloat( bin_combined_fake[syst].n + combined_fake[reg][syst]['sum'].n, bin_combined_fake[syst].s + combined_fake[reg][syst]['sum'].s )
                else:
                    bin_combined_fake[syst] = bin_combined_fake[syst] + combined_fake[reg][syst]['sum']

        for syst, val in bin_combined_fake.iteritems() :
            summed_el['Comb'+syst] = bin_combined_fake[syst]

        
        ## Keep all of the uncertainties, do not combine
        ## now simplify the uncertainties
        ## into data uncertainties
        ## electron uncertainties,
        ## and jet uncertainties
        #summed_el['CombStatSB'] = bin_combined_fake['statDataSB']
        #summed_el['CombStatSR'] = bin_combined_fake['statDataSR']
        #summed_el['CombEleFakeFF'] = bin_combined_fake['EleFakeFF']
        #
        ## collect jet uncertainties that are correlated 
        ## across channels
        ## all others should be set above
        #summed_el['CombJetCorr'] = ufloat( bin_combined_fake['statDataSB'].n, 0.0 )
        #for syst, val in bin_combined_fake.iteritems() :
        #    if syst == 'statDataSB' or syst == 'statDataSR' or syst == 'EleFakeFF' :
        #        continue

        #    summed_el['CombJetCorr'] += ufloat( 0.0, bin_combined_fake[syst].s )

    if zgg :
        return make_zgg_combination(results_final, jet_sum_mu, jet_sum_el, summed_mu, summed_el, pt_bins, eta_bins, outputDir=outputDir)
    else :
        return make_wgg_combination(results_final, jet_sum_mu, jet_sum_el, summed_mu, summed_el, pt_bins, eta_bins, outputDir=outputDir, combined_fake=combined_fake)

def make_wgg_combination( results_final, jet_sum_mu, jet_sum_el,summed_mu, summed_el, pt_bins, eta_bins, outputDir=None, combined_fake={} ) :

    # get histogram-based predictions
    summed_mu['Zgg']      = get_summed_sample( results_final['muon'],  'Zgg' , pt_bins, eta_bins, isCorr=True )
    summed_mu['ZggStat']  = get_summed_sample( results_final['muon'],  'ZggNoSyst' , pt_bins, eta_bins, isCorr=False )
    summed_mu['OtherDiPhoton']      = get_summed_sample( results_final['muon'],  'OtherDiPhoton' , pt_bins, eta_bins, isCorr=True )
    summed_mu['OtherDiPhotonStat']  = get_summed_sample( results_final['muon'],  'OtherDiPhotonNoSyst' , pt_bins, eta_bins, isCorr=False )
    summed_mu['Wgg']      = get_summed_sample( results_final['muon'],  'Wgg' , pt_bins, eta_bins, isCorr=True )
    summed_mu['Data']     = get_summed_sample( results_final['muon'],  'Data', pt_bins, eta_bins, isCorr=False )

    # get histogram-based predictions
    summed_el['Zgg']     = get_summed_sample( results_final['electron'],  'Zgg'    , pt_bins, eta_bins, isCorr=True )
    summed_el['ZggStat']  = get_summed_sample( results_final['electron'],  'ZggNoSyst', pt_bins, eta_bins, isCorr=False )
    summed_el['OtherDiPhoton']     = get_summed_sample( results_final['electron'],  'OtherDiPhoton'    , pt_bins, eta_bins, isCorr=True )
    summed_el['OtherDiPhotonStat']  = get_summed_sample( results_final['electron'],  'OtherDiPhotonNoSyst', pt_bins, eta_bins, isCorr=False )
    summed_el['Wgg']     = get_summed_sample( results_final['electron'],  'Wgg'    , pt_bins, eta_bins, isCorr=True )
    summed_el['Data']    = get_summed_sample( results_final['electron'],  'Data'   , pt_bins, eta_bins, isCorr=False )
    #summed_el['EleFake'] = get_summed_sample( results_final['electron'],  'EleFake', pt_bins, eta_bins, isCorr=False )

    # The uncertainties are provided as Stat only
    # flip to have them as syst only
    summed_mu['ZggSyst'] = make_uncert_compliment( summed_mu['Zgg'], summed_mu['ZggStat'], isCorr=True )
    summed_el['ZggSyst'] = make_uncert_compliment( summed_el['Zgg'], summed_el['ZggStat'], isCorr=True )
    summed_mu['OtherDiPhotonSyst'] = make_uncert_compliment( summed_mu['OtherDiPhoton'], summed_mu['OtherDiPhotonStat'], isCorr=True )
    summed_el['OtherDiPhotonSyst'] = make_uncert_compliment( summed_el['OtherDiPhoton'], summed_el['OtherDiPhotonStat'], isCorr=True )

    bkg_el = {}
    bkg_mu = {}
    # make the muon background sum
    # considering each uncetainty separately
    mu_zgg_nounc = ufloat( summed_mu['Zgg']['sum'].n, 0.0 )
    mu_odp_nounc = ufloat( summed_mu['OtherDiPhoton']['sum'].n, 0.0 )

    bkg_mu['statDataSB']         = summed_mu['statDataSB']['sum'] + mu_zgg_nounc + mu_odp_nounc
    bkg_mu['statDataSR']         = summed_mu['statDataSR']['sum'] + mu_zgg_nounc + mu_odp_nounc
    bkg_mu['JetFakeCrossCorr']   = summed_mu['crossCorr']['sum']  + mu_zgg_nounc + mu_odp_nounc
    bkg_mu['JetFakeSystBkg']     = summed_mu['systBkg']['sum']    + mu_zgg_nounc + mu_odp_nounc
    bkg_mu['JetFakeFakefake']    = summed_mu['fakefake']['sum']   + mu_zgg_nounc + mu_odp_nounc
    bkg_mu['JetFakeSystTemp']    = summed_mu['systTemp']['sum']   + mu_zgg_nounc + mu_odp_nounc
    bkg_mu['JetFakeStatTemp1D']  = summed_mu['statTemp1D']['sum'] + mu_zgg_nounc + mu_odp_nounc
    bkg_mu['JetFakeStatTempFF']  = summed_mu['statTempFF']['sum'] + mu_zgg_nounc + mu_odp_nounc
    bkg_mu['ZggStat']            = ufloat( summed_mu['statDataSB']['sum'].n, 0.0) +  summed_mu['ZggStat']['sum'] + mu_odp_nounc
    bkg_mu['ZggSyst']            = ufloat( summed_mu['statDataSB']['sum'].n, 0.0) +  summed_mu['ZggSyst']['sum'] + mu_odp_nounc
    bkg_mu['OtherDiPhotonStat']  = ufloat( summed_mu['statDataSB']['sum'].n, 0.0) +  summed_mu['OtherDiPhotonStat']['sum'] + mu_zgg_nounc
    bkg_mu['OtherDiPhotonSyst']  = ufloat( summed_mu['statDataSB']['sum'].n, 0.0) +  summed_mu['OtherDiPhotonSyst']['sum'] + mu_zgg_nounc

    # lumi uncertainty applies to sum of
    # MC backgrounds
    mc_sum_nouncert = summed_mu['Zgg']['sum'].n + summed_mu['OtherDiPhoton']['sum'].n
    mc_sum = ufloat( mc_sum_nouncert, 0.026 * mc_sum_nouncert)
    bkg_mu['lumi']               = ufloat( summed_mu['statDataSB']['sum'].n, 0.0) +  mc_sum 

    # make the electron background sum
    # considering each uncetainty separately
    # summed_el already contains jet + el
    el_zgg_nounc = ufloat( summed_el['Zgg']['sum'].n, 0.0 )
    el_odp_nounc = ufloat( summed_el['OtherDiPhoton']['sum'].n, 0.0 )
    bkg_el['statDataSB']        = summed_el['CombstatDataSB'] + el_zgg_nounc + el_odp_nounc
    bkg_el['statDataSR']        = summed_el['CombstatDataSR'] + el_zgg_nounc + el_odp_nounc
    bkg_el['JetFakeCrossCorr']  = summed_el['CombcrossCorr']  + el_zgg_nounc + el_odp_nounc
    bkg_el['JetFakeSystBkg']    = summed_el['CombsystBkg']    + el_zgg_nounc + el_odp_nounc
    bkg_el['JetFakeSystTemp']   = summed_el['CombsystTemp']   + el_zgg_nounc + el_odp_nounc
    bkg_el['JetFakeStatTemp1D'] = summed_el['CombstatTemp1D'] + el_zgg_nounc + el_odp_nounc
    bkg_el['JetFakeStatTempFF'] = summed_el['CombstatTempFF'] + el_zgg_nounc + el_odp_nounc
    bkg_el['JetFakeFakefake'] = summed_el['Combfakefake'] + el_zgg_nounc + el_odp_nounc
    bkg_el['EleFakeFF']         = summed_el['CombEleFakeFF']  + el_zgg_nounc + el_odp_nounc
    bkg_el['ZggStat']           = ufloat(summed_el['CombstatDataSB'].n, 0.0) + summed_el['ZggStat']['sum'] + el_odp_nounc
    bkg_el['ZggSyst']           = ufloat(summed_el['CombstatDataSB'].n, 0.0) + summed_el['ZggSyst']['sum'] + el_odp_nounc
    bkg_el['OtherDiPhotonStat'] = ufloat(summed_el['CombstatDataSB'].n, 0.0) + summed_el['OtherDiPhotonStat']['sum'] + el_zgg_nounc
    bkg_el['OtherDiPhotonSyst'] = ufloat(summed_el['CombstatDataSB'].n, 0.0) + summed_el['OtherDiPhotonSyst']['sum'] + el_zgg_nounc

    # lumi uncertainty applies to sum of
    # MC backgrounds
    mc_sum_nouncert = summed_el['Zgg']['sum'].n + summed_el['OtherDiPhoton']['sum'].n
    mc_sum = ufloat( mc_sum_nouncert, 0.026 * mc_sum_nouncert )
    bkg_el['lumi']              = ufloat( summed_el['CombstatDataSB'].n, 0.0) +  mc_sum 

    lumi = ufloat( 19.4, 19.4*0.026 )

    exp_mu = bkg_mu['statDataSB'] + summed_mu['Wgg']['sum']
    exp_el = bkg_el['statDataSB'] + summed_el['Wgg']['sum']
    xs_mu_sig =  (ufloat( exp_mu.n, math.sqrt(exp_mu.n) ) - bkg_mu['statDataSB'])/ ( comb_acceptance['muon']['stat'] * lumi )
    xs_el_sig =  (ufloat(exp_el.n, math.sqrt(exp_el.n) ) - bkg_el['statDataSB'] )/ ( comb_acceptance['electron']['stat'] * lumi )
    xs_mu = {}
    xs_el = {}

    # combine the SR and SB uncertainties
    # the SR uncertainties are correlated
    # between the data and jetSR
    # the SB are uncorrelated
    # calculate data - bkg, using correlated SR uncertainties
    numerator_mu_sr = ufloat( summed_mu['Data']['sum'].n - bkg_mu['statDataSR'].n, summed_mu['Data']['sum'].s - bkg_mu['statDataSR'].s )
    # add in uncorrelated SB uncertainties
    numerator_mu_comb = numerator_mu_sr + ufloat( 0.0, summed_mu['statDataSB']['sum'].s )

    xs_mu_data_nounc = ufloat( summed_mu['Data']['sum'].n,0.0 )
    xs_mu_acc_nounc  = ufloat( comb_acceptance['muon']['stat'].n, 0.0)
    xs_mu_bkg_nounc  = ufloat( bkg_mu['statDataSB'].n, 0.0 )
    xs_mu_lumi_nounc = ufloat( lumi.n, 0.0 )


    xs_mu['statData']    = ( numerator_mu_comb )                                       / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['ZggStat']     = ( xs_mu_data_nounc - bkg_mu['ZggStat'])                     / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['ZggSyst']     = ( xs_mu_data_nounc - bkg_mu['ZggSyst'])                     / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['OtherDiPhotonStat']     = ( xs_mu_data_nounc - bkg_mu['OtherDiPhotonStat']) / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['OtherDiPhotonSyst']     = ( xs_mu_data_nounc - bkg_mu['OtherDiPhotonSyst']) / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeCrossCorr'] = ( xs_mu_data_nounc - bkg_mu['JetFakeCrossCorr'])       / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeSystBkg'] = ( xs_mu_data_nounc - bkg_mu['JetFakeSystBkg'])           / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeSystTemp'] = ( xs_mu_data_nounc - bkg_mu['JetFakeSystTemp'])         / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeStatTemp1D'] = ( xs_mu_data_nounc - bkg_mu['JetFakeStatTemp1D'])     / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeStatTempFF'] = ( xs_mu_data_nounc - bkg_mu['JetFakeStatTempFF'])     / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeFakefake'] = ( xs_mu_data_nounc - bkg_mu['JetFakeFakefake'])     / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['lumi']        = ( xs_mu_data_nounc - bkg_mu['lumi'])                        / ( xs_mu_acc_nounc*lumi)
    xs_mu['AccStat']     = ( xs_mu_data_nounc - xs_mu_bkg_nounc)                       / ( comb_acceptance['muon']['stat']*xs_mu_lumi_nounc)
    xs_mu['AccLeptonID']  = ( xs_mu_data_nounc - xs_mu_bkg_nounc)                       / ( comb_acceptance['muon']['LeptonID']*xs_mu_lumi_nounc)
    xs_mu['AccPhotonID']   = ( xs_mu_data_nounc - xs_mu_bkg_nounc)                       / ( comb_acceptance['muon']['PhotonID']*xs_mu_lumi_nounc)
    xs_mu['AccPhotonEV']   = ( xs_mu_data_nounc - xs_mu_bkg_nounc)                       / ( comb_acceptance['muon']['PhotonEV']*xs_mu_lumi_nounc)
    xs_mu['AccEGScale']   = ( xs_mu_data_nounc - xs_mu_bkg_nounc)                       / ( comb_acceptance['muon']['EGScale']*xs_mu_lumi_nounc)
    xs_mu['AccMuScale']   = ( xs_mu_data_nounc - xs_mu_bkg_nounc)                       / ( comb_acceptance['muon']['MuScale']*xs_mu_lumi_nounc)
    xs_mu['AccMET']   = ( xs_mu_data_nounc - xs_mu_bkg_nounc)                       / ( comb_acceptance['muon']['MET']*xs_mu_lumi_nounc)
    xs_mu['AccPileup']   = ( xs_mu_data_nounc - xs_mu_bkg_nounc)                       / ( comb_acceptance['muon']['Pileup']*xs_mu_lumi_nounc)
    xs_mu['AccTheory']   = ( xs_mu_data_nounc - xs_mu_bkg_nounc)                       / ( comb_acceptance['muon']['Theory']*xs_mu_lumi_nounc)
    # copy the CV with no uncertainty
    xs_mu['EleFakeFF']  = ufloat( xs_mu['statData'].n, 0.0 )

    # combine the SR and SB uncertainties
    # the SR uncertainties are correlated
    # between the data and jetSR
    # the SB are uncorrelated
    # calculate data - bkg, using correlated SR uncertainties
    numerator_el_sr = ufloat( summed_el['Data']['sum'].n - bkg_el['statDataSR'].n, summed_el['Data']['sum'].s - bkg_el['statDataSR'].s )
    # add in uncorrelated SB uncertainties
    numerator_el_comb = numerator_el_sr + ufloat( 0.0, bkg_el['statDataSB'].s )

    xs_el_data_nounc = ufloat( summed_el['Data']['sum'].n,0.0 )
    xs_el_acc_nounc  = ufloat( comb_acceptance['electron']['stat'].n, 0.0)
    xs_el_bkg_nounc  = ufloat( bkg_el['statDataSB'].n, 0.0 )
    xs_el_lumi_nounc = ufloat( lumi.n, 0.0 )

    xs_el['statData']          = ( numerator_el_comb )                             / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['ZggStat']           = ( xs_el_data_nounc - bkg_el['ZggStat'])           / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['ZggSyst']           = ( xs_el_data_nounc - bkg_el['ZggSyst'])           / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['OtherDiPhotonStat'] = ( xs_el_data_nounc - bkg_el['OtherDiPhotonStat']) / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['OtherDiPhotonSyst'] = ( xs_el_data_nounc - bkg_el['OtherDiPhotonSyst']) / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeCrossCorr']  = ( xs_el_data_nounc - bkg_el['JetFakeCrossCorr'])  / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeSystBkg']    = ( xs_el_data_nounc - bkg_el['JetFakeSystBkg'])    / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeSystTemp']   = ( xs_el_data_nounc - bkg_el['JetFakeSystTemp'])   / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeStatTemp1D'] = ( xs_el_data_nounc - bkg_el['JetFakeStatTemp1D']) / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeStatTempFF'] = ( xs_el_data_nounc - bkg_el['JetFakeStatTempFF']) / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeFakefake'] = ( xs_el_data_nounc - bkg_el['JetFakeFakefake']) / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['EleFakeFF']         = ( xs_el_data_nounc - bkg_el['EleFakeFF'])         / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['lumi']              = ( xs_el_data_nounc - bkg_el['lumi'])              / ( xs_el_acc_nounc*lumi)
    xs_el['AccStat']           = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance['electron']['stat']   *xs_el_lumi_nounc)
    xs_el['AccLeptonID']        = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance['electron']['LeptonID']*xs_el_lumi_nounc)
    xs_el['AccPhotonID']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance['electron']['PhotonID'] *xs_el_lumi_nounc)
    xs_el['AccPhotonEV']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance['electron']['PhotonEV'] *xs_el_lumi_nounc)
    xs_el['AccEGScale']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance['electron']['EGScale'] *xs_el_lumi_nounc)
    xs_el['AccMuScale']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance['electron']['MuScale'] *xs_el_lumi_nounc)
    xs_el['AccMET']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance['electron']['MET'] *xs_el_lumi_nounc)
    xs_el['AccPileup']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance['electron']['Pileup'] *xs_el_lumi_nounc)
    xs_el['AccTheory']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance['electron']['Theory'] *xs_el_lumi_nounc)

    print 'Muon, N Data = %d, N Sig = %f, n Bkg = %s '      %( summed_mu['Data']['sum'].n, summed_mu['Wgg']['sum'].n, bkg_mu )
    print 'Electron , N Data = %d, N Sig = %f, n Bkg = %s ' %( summed_el['Data']['sum'].n, summed_el['Wgg']['sum'].n, bkg_el )
    #print 'S/sigma(B), mu =  %f ' %( summed_mu['Wgg']['sum'].n / bkg_mu.s )
    #print 'S/sigma(B), el =  %f ' %( summed_el['Wgg']['sum'].n / bkg_el.s )
    print 'xs_mu_sig = %s, frac unc = %f' %( xs_mu_sig, xs_mu_sig.s/xs_mu_sig.n)
    print 'xs_el_sig = %s, frac unc = %f' %( xs_el_sig, xs_el_sig.s/xs_el_sig.n)

    comb_xs_mu = ufloat( xs_mu['statData'].n, 0.0 )
    comb_xs_el = ufloat( xs_el['statData'].n, 0.0 )

    for syst, val in xs_mu.iteritems() :
        comb_xs_mu += ufloat( 0.0, val.s )
    for syst, val in xs_el.iteritems() :
        comb_xs_el += ufloat( 0.0, val.s )

    print 'Final xs_mu = %s' %comb_xs_mu
    print 'Individual xs mu'
    for key, val in xs_mu.iteritems() :
        print '%s - %s' %( key, val )
    print 'Final xs_el = %s' %comb_xs_el

    xs_mu['central_value'] = comb_xs_mu
    xs_el['central_value'] = comb_xs_el

    ch_correlations  = {
                        'statData'  : False, 
                        'JetFakeCrossCorr' : False, 
                        'JetFakeSystBkg' : True, 
                        'JetFakeSystTemp' : True, 
                        'JetFakeStatTemp1D' : True, 
                        'JetFakeStatTempFF' : True, 
                        'JetFakeFakefake' : False, 
                        'ZggStat'     : False, 
                        'ZggSyst'     : True, 
                        'OtherDiPhotonStat'     : False, 
                        'OtherDiPhotonSyst'     : True, 
                        'lumi'        : True,
                        'AccStat'     : False,
                        'AccLeptonID'  : False,
                        'AccPhotonID'   : True,
                        'AccPhotonEV'   : False,
                        'AccEGScale'   : True,
                        'AccMuScale'   : False,
                        'AccMET'   : True,
                        'AccPileup'   : True,
                        'AccTheory'   : True,
                       }
    
    non_blue_systs = {'EleFakeFF' :xs_el['EleFakeFF'] }

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

        validx = { 0 : xs_mu[syst], 1 : xs_el[syst] }
        matrix  = []

        for i in range( 0, n_ch ) :
            list_i = [0]*n_ch
            for j in range( 0, n_ch ) :
                entry  = validx[i].s*validx[j].s

                if i != j and not is_corr :
                    entry = 0

                list_i[j]  = entry

            matrix.append( list_i )

        print 'syst = %s, corr? %s ' %( syst, is_corr )
        print matrix


        xs_calc.AddErrorMatrix( matrix )
        if syst in calc_indiv :
            calc_indiv[syst].AddErrorMatrix( matrix)

    combined_value = xs_calc.CalculateCombinedValue()
    combined_error = xs_calc.CalculateCombinedUncertainty()

    combined_alphas = xs_calc.GetAlphas()
    for icalc in calc_indiv.values() :
        icalc.SetAlphas( combined_alphas )

    errsq_extra = 0.0
    for syst, val in non_blue_systs.iteritems() :
        errsq_extra += ( val.s/val.n ) * ( val.s/val.n )
    combined_error = math.sqrt( combined_error*combined_error +  errsq_extra )

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

    for syst in non_blue_systs.keys() :
        comb_results['isCorr'][syst] = False

    for syst, val in non_blue_systs.iteritems() :
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

    output_results['combined_fake'] = combined_fake

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
    summed_mu['OtherDiPhoton']      = get_summed_sample( results_final['muon'],  'OtherDiPhoton' , pt_bins, eta_bins, isCorr=True )
    summed_mu['OtherDiPhotonStat']  = get_summed_sample( results_final['muon'],  'OtherDiPhotonNoSyst' , pt_bins, eta_bins, isCorr=False )

    summed_el['Zgg']     = get_summed_sample( results_final['electron'],  'Zgg'    , pt_bins, eta_bins, isCorr=True )
    summed_el['Data']    = get_summed_sample( results_final['electron'],  'Data'   , pt_bins, eta_bins, isCorr=False )
    summed_el['OtherDiPhoton']     = get_summed_sample( results_final['electron'],  'OtherDiPhoton'    , pt_bins, eta_bins, isCorr=True )
    summed_el['OtherDiPhotonStat']  = get_summed_sample( results_final['electron'],  'OtherDiPhotonNoSyst', pt_bins, eta_bins, isCorr=False )

    # The uncertainties are provided as Stat only
    # flip to have them as syst only
    summed_mu['OtherDiPhotonSyst'] = make_uncert_compliment( summed_mu['OtherDiPhoton'], summed_mu['OtherDiPhotonStat'], isCorr=True )
    summed_el['OtherDiPhotonSyst'] = make_uncert_compliment( summed_el['OtherDiPhoton'], summed_el['OtherDiPhotonStat'], isCorr=True )

    bkg_el = {}
    bkg_mu = {}

    #-----------------------------------
    # Muon Bkg sum
    #-----------------------------------
    mu_odp_nounc = ufloat( summed_mu['OtherDiPhoton']['sum'].n, 0.0 )

    bkg_mu['statDataSR']        = summed_mu['statDataSR']['sum'] + mu_odp_nounc
    bkg_mu['statDataSB']        = summed_mu['statDataSB']['sum'] + mu_odp_nounc

    bkg_mu['JetFakeCrossCorr']  = summed_mu['crossCorr']['sum']   + mu_odp_nounc
    bkg_mu['JetFakeSystBkg']    = summed_mu['systBkg']['sum']     + mu_odp_nounc
    bkg_mu['JetFakeFakefake']   = summed_mu['fakefake']['sum']    + mu_odp_nounc
    bkg_mu['JetFakeSystTemp']   = summed_mu['systTemp']['sum']    + mu_odp_nounc
    bkg_mu['JetFakeStatTemp1D'] = summed_mu['statTemp1D']['sum']  + mu_odp_nounc
    bkg_mu['JetFakeStatTempFF'] = summed_mu['statTempFF']['sum']  + mu_odp_nounc

    bkg_mu['OtherDiPhotonStat'] = ufloat( summed_mu['statDataSB']['sum'].n, 0.0) +  summed_mu['OtherDiPhotonStat']['sum']
    bkg_mu['OtherDiPhotonSyst'] = ufloat( summed_mu['statDataSB']['sum'].n, 0.0) +  summed_mu['OtherDiPhotonSyst']['sum']
    bkg_mu['lumi']              = ufloat( summed_mu['statDataSB']['sum'].n, 0.0) + ufloat( summed_mu['OtherDiPhoton']['sum'].n, summed_mu['OtherDiPhoton']['sum'].n*0.026 )


    #-----------------------------------
    # Electron Bkg sum
    #-----------------------------------
    el_odp_nounc = ufloat( summed_el['OtherDiPhoton']['sum'].n, 0.0 )

    bkg_el['statDataSR']        = summed_el['statDataSR']['sum'] + el_odp_nounc
    bkg_el['statDataSB']        = summed_el['statDataSB']['sum'] + el_odp_nounc

    bkg_el['JetFakeCrossCorr']  = summed_el['crossCorr']['sum']   + el_odp_nounc
    bkg_el['JetFakeSystBkg']    = summed_el['systBkg']['sum']     + el_odp_nounc
    bkg_el['JetFakeFakefake']   = summed_el['fakefake']['sum']    + el_odp_nounc
    bkg_el['JetFakeSystTemp']   = summed_el['systTemp']['sum']    + el_odp_nounc
    bkg_el['JetFakeStatTemp1D'] = summed_el['statTemp1D']['sum']  + el_odp_nounc
    bkg_el['JetFakeStatTempFF'] = summed_el['statTempFF']['sum']  + el_odp_nounc

    bkg_el['OtherDiPhotonStat'] = ufloat( summed_el['statDataSB']['sum'].n, 0.0) +  summed_el['OtherDiPhotonStat']['sum']
    bkg_el['OtherDiPhotonSyst'] = ufloat( summed_el['statDataSB']['sum'].n, 0.0) +  summed_el['OtherDiPhotonSyst']['sum']
    bkg_el['lumi']              = ufloat( summed_el['statDataSB']['sum'].n, 0.0) + ufloat( summed_el['OtherDiPhoton']['sum'].n, summed_el['OtherDiPhoton']['sum'].n*0.026 )


    lumi = ufloat( 19.4, 19.4*0.026 )

    exp_mu = bkg_mu['statDataSB'] + summed_mu['Zgg']['sum']
    exp_el = bkg_el['statDataSB'] + summed_el['Zgg']['sum']

    xs_mu_sig =  (ufloat( exp_mu.n, math.sqrt(exp_mu.n) ) - bkg_mu['statDataSB'])/ ( comb_acceptance_zgg['muon']['stat'] * lumi )
    xs_el_sig =  (ufloat(exp_el.n, math.sqrt(exp_el.n) ) - bkg_el['statDataSB'] )/ ( comb_acceptance_zgg['electron']['stat'] * lumi )

    xs_mu = {}
    xs_el = {}

    # combine the SR and SB uncertainties
    # the SR uncertainties are correlated
    # between the data and jetSR
    # the SB are uncorrelated
    # calculate data - bkg, using correlated SR uncertainties
    numerator_mu_sr = ufloat( summed_mu['Data']['sum'].n - bkg_mu['statDataSR'].n, summed_mu['Data']['sum'].s - bkg_mu['statDataSR'].s )
    # add in uncorrelated SB uncertainties
    numerator_mu_comb = numerator_mu_sr + ufloat( 0.0, summed_mu['statDataSB']['sum'].s )

    xs_mu_data_nounc  = ufloat( summed_mu['Data']['sum'].n, 0.0 )
    xs_mu_acc_nounc   = ufloat( comb_acceptance_zgg['muon']['stat'].n, 0.0 )
    xs_mu_bkg_nounc   = ufloat( bkg_mu['statDataSB'].n, 0.0 )
    xs_mu_lumi_nounc  = ufloat( lumi.n, 0.0 )

    xs_mu['statData']          = ( numerator_mu_comb )                             / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['OtherDiPhotonStat'] = ( xs_mu_data_nounc - bkg_mu['OtherDiPhotonStat']) / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['OtherDiPhotonSyst'] = ( xs_mu_data_nounc - bkg_mu['OtherDiPhotonSyst']) / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeCrossCorr']  = ( xs_mu_data_nounc - bkg_mu['JetFakeCrossCorr'])  / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeSystBkg']    = ( xs_mu_data_nounc - bkg_mu['JetFakeSystBkg'])    / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeFakefake']   = ( xs_mu_data_nounc - bkg_mu['JetFakeFakefake'])   / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeSystTemp']   = ( xs_mu_data_nounc - bkg_mu['JetFakeSystTemp'])   / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeStatTemp1D'] = ( xs_mu_data_nounc - bkg_mu['JetFakeStatTemp1D']) / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['JetFakeStatTempFF'] = ( xs_mu_data_nounc - bkg_mu['JetFakeStatTempFF']) / ( xs_mu_acc_nounc*xs_mu_lumi_nounc )
    xs_mu['lumi']              = ( xs_mu_data_nounc - bkg_mu['lumi'] )             / ( xs_mu_acc_nounc*lumi)
    xs_mu['AccStat']           = ( xs_mu_data_nounc - xs_mu_bkg_nounc)             / ( comb_acceptance_zgg['muon']['stat']   *xs_mu_lumi_nounc)
    xs_mu['AccLeptonID']        = ( xs_mu_data_nounc - xs_mu_bkg_nounc)             / ( comb_acceptance_zgg['muon']['LeptonID']*xs_mu_lumi_nounc)
    xs_mu['AccPhotonID']         = ( xs_mu_data_nounc - xs_mu_bkg_nounc)             / ( comb_acceptance_zgg['muon']['PhotonID']*xs_mu_lumi_nounc)
    xs_mu['AccEGScale']         = ( xs_mu_data_nounc - xs_mu_bkg_nounc)             / ( comb_acceptance_zgg['muon']['EGScale']*xs_mu_lumi_nounc)
    xs_mu['AccMuScale']         = ( xs_mu_data_nounc - xs_mu_bkg_nounc)             / ( comb_acceptance_zgg['muon']['MuScale']*xs_mu_lumi_nounc)
    xs_mu['AccPileup']         = ( xs_mu_data_nounc - xs_mu_bkg_nounc)             / ( comb_acceptance_zgg['muon']['Pileup']*xs_mu_lumi_nounc)
    xs_mu['AccTheory']         = ( xs_mu_data_nounc - xs_mu_bkg_nounc)             / ( comb_acceptance_zgg['muon']['Theory']*xs_mu_lumi_nounc)

    # combine the SR and SB uncertainties
    # the SR uncertainties are correlated
    # between the data and jetSR
    # the SB are uncorrelated
    # calculate data - bkg, using correlated SR uncertainties
    numerator_el_sr = ufloat( summed_el['Data']['sum'].n - bkg_el['statDataSR'].n, summed_el['Data']['sum'].s - bkg_el['statDataSR'].s )
    # add in uncorrelated SB uncertainties
    numerator_el_comb = numerator_el_sr + ufloat( 0.0, summed_el['statDataSB']['sum'].s )

    xs_el_data_nounc  = ufloat( summed_el['Data']['sum'].n, 0.0 )
    xs_el_acc_nounc   = ufloat( comb_acceptance_zgg['electron']['stat'].n, 0.0 )
    xs_el_bkg_nounc   = ufloat( bkg_el['statDataSB'].n, 0.0 )
    xs_el_lumi_nounc  = ufloat( lumi.n, 0.0 )

    xs_el['statData']          = ( numerator_el_comb )                             / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['OtherDiPhotonStat'] = ( xs_el_data_nounc - bkg_el['OtherDiPhotonStat']) / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['OtherDiPhotonSyst'] = ( xs_el_data_nounc - bkg_el['OtherDiPhotonSyst']) / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeCrossCorr']  = ( xs_el_data_nounc - bkg_el['JetFakeCrossCorr'])  / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeSystBkg']    = ( xs_el_data_nounc - bkg_el['JetFakeSystBkg'])    / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeSystTemp']   = ( xs_el_data_nounc - bkg_el['JetFakeSystTemp'])   / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeFakefake']   = ( xs_el_data_nounc - bkg_el['JetFakeFakefake'])   / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeStatTemp1D'] = ( xs_el_data_nounc - bkg_el['JetFakeStatTemp1D']) / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['JetFakeStatTempFF'] = ( xs_el_data_nounc - bkg_el['JetFakeStatTempFF']) / ( xs_el_acc_nounc*xs_el_lumi_nounc )
    xs_el['lumi']              = ( xs_el_data_nounc - bkg_el['lumi'] )             / ( xs_el_acc_nounc*lumi)
    xs_el['AccStat']           = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance_zgg['electron']['stat']   *xs_el_lumi_nounc)
    xs_el['AccLeptonID']        = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance_zgg['electron']['LeptonID']*xs_el_lumi_nounc)
    xs_el['AccPhotonID']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance_zgg['electron']['PhotonID']*xs_el_lumi_nounc)
    xs_el['AccEGScale']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance_zgg['electron']['EGScale']*xs_el_lumi_nounc)
    xs_el['AccMuScale']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance_zgg['electron']['MuScale']*xs_el_lumi_nounc)
    xs_el['AccPileup']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance_zgg['electron']['Pileup']*xs_el_lumi_nounc)
    xs_el['AccTheory']         = ( xs_el_data_nounc - xs_el_bkg_nounc)             / ( comb_acceptance_zgg['electron']['Theory']*xs_el_lumi_nounc)


    print 'Muon, N Data = %d, N Sig = %f, n Bkg = %s '      %( summed_mu['Data']['sum'].n, summed_mu['Zgg']['sum'].n, bkg_mu )
    print 'Electron , N Data = %d, N Sig = %f, n Bkg = %s ' %( summed_el['Data']['sum'].n, summed_el['Zgg']['sum'].n, bkg_el )
    #print 'S/sigma(B), mu =  %f ' %( summed_mu['Wgg']['sum'].n / bkg_mu.s )
    #print 'S/sigma(B), el =  %f ' %( summed_el['Wgg']['sum'].n / bkg_el.s )
    print 'xs_mu_sig = %s, frac unc = %f' %( xs_mu_sig, xs_mu_sig.s/xs_mu_sig.n)
    print 'xs_el_sig = %s, frac unc = %f' %( xs_el_sig, xs_el_sig.s/xs_el_sig.n)


    comb_xs_mu = ufloat( xs_mu['statData'].n, 0.0 )
    comb_xs_el = ufloat( xs_el['statData'].n, 0.0 )

    for syst, val in xs_mu.iteritems() :
        comb_xs_mu += ufloat( 0.0, val.s )
    for syst, val in xs_el.iteritems() :
        comb_xs_el += ufloat( 0.0, val.s )


    print 'Final xs_mu = ${:.5ufL}$' .format(comb_xs_mu)
    print 'Final xs_el = ${:.5ufL}$' .format(comb_xs_el)

    xs_mu['central_value'] = comb_xs_mu
    xs_el['central_value'] = comb_xs_el

    ch_correlations  = {'statData'    : False, 
                        'JetFakeCrossCorr' : True, 
                        'JetFakeSystBkg' : True, 
                        'JetFakeSystTemp' : True, 
                        'JetFakeStatTemp1D' : True, 
                        'JetFakeStatTempFF' : True, 
                        'JetFakeFakefake' : False, 
                        'OtherDiPhotonStat'     : False, 
                        'OtherDiPhotonSyst'     : True, 
                        'lumi'        : True,
                        'AccStat'     : False,
                        'AccLeptonID'  : False,
                        'AccPhotonID'   : True,
                        'AccEGScale'   : True,
                        'AccMuScale'   : False,
                        'AccPileup'   : True,
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

        validx = { 0 : xs_mu[syst].s, 1 : xs_el[syst].s }
        matrix  = []
        for i in range( 0, n_ch ) :
            list_i = [0]*n_ch
            for j in range( 0, n_ch ) :
                entry  = validx[i]*validx[j]

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

    for syst in extra_systs.keys() :
        comb_results['isCorr'][syst] = False
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

def collect_jet_systs( jet_sum, all_systs) :

    jet_tot_temp1d = {'sum' : ufloat( 0.0, 0.0), 'bins' : {} }

    summed = {}

    for syst in all_systs  :
        summed[syst] = { 'sum' : ufloat( 0.0, 0.0 ), 'bins' : {} }

    for idx, syst in enumerate( all_systs ) :
        summed[syst]['sum'] = summed[syst]['sum'] + jet_sum['sum'][syst] 
        summed[syst]['isCorr'] =  jet_sum['isCorr'][syst]
        for rbin in jet_sum['bins'].keys() :
            summed[syst]['bins'].setdefault( rbin, {} )
            summed[syst]['bins'][rbin] = jet_sum['bins'][rbin][syst]

    
    for rbin in jet_sum['bins'].keys() :
        jet_tot_temp1d['bins'][rbin] = jet_sum['bins'][rbin]['statTempTight']
        jet_tot_temp1d['bins'][rbin] = jet_tot_temp1d['bins'][rbin]+ ufloat( 0.0, jet_sum['bins'][rbin]['statTempLoose'].s )

    jet_tot_temp1d['sum'] = jet_sum['sum']['statTempTight']
    jet_tot_temp1d['sum'] += ufloat( 0.0, jet_sum['sum']['statTempLoose'].s )
    jet_tot_temp1d['isCorr'] = False

    summed['statTemp1D']         = jet_tot_temp1d

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



#def calc_xs_old( results ) :
#
#    pt_bins = ['15', '25', '40', '70', 'max']
#    #pt_bins = ['40', '70', 'max']
#
#    lumi = ufloat( 19.4, 19.4*0.026 )
#    #lumi = ufloat( 19.4, 0.0 )
#    xs_data = {}
#    for ch, res in results.iteritems() :
#
#        print '***********************'
#        print 'Channel %s' %ch
#        print '***********************'
#
#        all_xs = []
#
#        xs_data[ch] = {}
#
#
#        for idx, ptmin in enumerate( pt_bins[:-1] ) :
#
#            ptmax = pt_bins[idx+1]
#
#            acceptance = acceptances[ch][(ptmin,ptmax)]
#
#            data = res['detail']['Data']['bins'][str(idx+1)]['val']
#
#            bkg = ufloat( 0.0, 0.0 )
#            sig = ufloat( 0.0, 0.0 )
#
#            bkg = bkg + res['detail']['Zgg']['bins'][str(idx+1)]['val']
#            bkg = bkg + res['detail']['JetFake']['bins'][str(idx+1)]['val']
#            print '********************FIX*****************'
#            #bkg = bkg + res['detail']['OtherDiPhoton']['bins'][str(idx+1)]['val']
#
#            if ch=='electron' :
#                bkg = bkg + res['detail']['EleFake']['bins'][str(idx+1)]['val']
#
#            sig = sig + res['detail']['Wgg']['bins'][str(idx+1)]['val']
#            sig = ufloat( sig.n, math.sqrt( sig.n ) )
#
#            bkg = ufloat( bkg.n, 0.0 )
#
#            #data = ufloat( data.n , 0.0 )
#
#            data_minus_bkg = data - bkg
#
#
#            cross_section = ( data_minus_bkg ) / ( acceptance * lumi )
#            cross_section_exp = ( sig + ufloat( 0.0, bkg.s) ) / ( acceptance * lumi )
#
#            xs_data[ch][( ptmin, ptmax)] = {'acceptance' : acceptance, 'bkg' : bkg, 'sig' : sig, 'data' : data, 'cross_section' : cross_section, 'cross_section_exp' : cross_section_exp }
#
#            all_xs.append(cross_section)
#
#            print 'Pt bin : %s - %s' %( ptmin, ptmax )
#            print 'Data = %s, Background = %s, Diff = %s' %(data, bkg, data_minus_bkg)
#            print 'Signal = %s' %sig
#            print 'acceptance = %s ' %acceptance
#            print 'Expected cross section = %s fb' %cross_section_exp
#            print 'Cross section = %s fb' %cross_section
#
#
#        sum_xs = reduce( lambda x, y : x + y, all_xs )
#
#        print 'Summed cross section = %s fb' %sum_xs
#
#
#    rev_ptbins = list( pt_bins )
#    rev_ptbins.reverse()
#    cross_section_tot = ufloat( 0.0, 0.0 )
#    cross_section_tot_exp = ufloat( 0.0, 0.0 )
#    for ch in results.keys() :
#        cross_section = ufloat( 0.0, 0.0 )
#        cross_section_exp = ufloat( 0.0, 0.0 )
#
#        print 'Reverse cumulative sum, channel = %s' %ch
#        
#        for idx, ptmax in enumerate( rev_ptbins[:-1] ) :
#            ptmin = rev_ptbins[idx+1]
#
#            cross_section = cross_section + xs_data[ch][( ptmin, ptmax )]['cross_section']
#            cross_section_exp = cross_section_exp + xs_data[ch][( ptmin, ptmax )]['cross_section_exp']
#
#
#            print 'Pt bin : %s - %s' %( ptmin, ptmax )
#            print 'Expected cross section = %s' %cross_section_exp
#            print 'Cross section = %s' %cross_section
#            if ptmin == '15' :
#                cross_section_tot = cross_section_tot + cross_section
#                cross_section_tot_exp = cross_section_tot_exp   + cross_section_exp
#
#    print 'Total Expected cross section = %s' %cross_section_tot_exp
#    print 'Total Cross section = %s' %cross_section_tot
#
#
#        
#    ofile = open( '%s/cross_section_results.pickle' %(options.baseDir ), 'w' )
#
#    pickle.dump(xs_data, ofile )
#
#    ofile.close()

def resolve_negatives( val ) :

    if val.n >= 0 :
        return val
    else :

        if math.fabs(val.s) > math.fabs(val.n) :
            return ufloat( 0.0, val.s )
        else :
            return ufloat( 0.0, math.fabs(val.n) )



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
