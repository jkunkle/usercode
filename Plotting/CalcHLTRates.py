import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import pickle
import os
import math
from collections import OrderedDict
from uncertainties import ufloat

from SampleManager import SampleManager
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--baseDir'  ,  dest='baseDir'  , default=None, help='Path to ntuples')
parser.add_argument( '--outputDir'  ,  dest='outputDir'  , default=None, help='Path to output directory, save plots here')

options = parser.parse_args()

ROOT.gROOT.SetBatch(False)
if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)

_TREENAME = 'HltTree'
_FILENAME = 'hltbits'
_XSFILE   = 'cross_sections/trig_rates.py'
_LUMI     = 36000
_MODULE = 'Modules/Rates.py'


triggers = [
            {'trigger' : 'HLT_Photon22_v6'                         , 'L1Seeds' : [] },
            {'trigger' : 'HLT_Photon22_R9Id90_HE10_IsoM_v7'        , 'L1Seeds' : [] },
            {'trigger' : 'HLT_SinglePhoton20NonIso_v0'             , 'L1Seeds' : [] },
            {'trigger' : 'HLT_SinglePhoton20CaloIdL_v0'            , 'L1Seeds' : [] },
            {'trigger' : 'HLT_SinglePhoton20CaloIsoM_v0'           , 'L1Seeds' : [] },
            {'trigger' : 'HLT_SinglePhoton20CaloIdLCaloIsoM_v0'    , 'L1Seeds' : [] },
            {'trigger' : 'HLT_SinglePhoton30NonIso_v0'             , 'L1Seeds' : [] },
            {'trigger' : 'HLT_SinglePhoton30CaloIdL_v0'            , 'L1Seeds' : [] },
            {'trigger' : 'HLT_SinglePhoton30CaloIsoM_v0'           , 'L1Seeds' : [] },
            {'trigger' : 'HLT_SinglePhoton30CaloIdLCaloIsoM_v0'    , 'L1Seeds' : [] },
            {'trigger' : 'HLT_DoublePhoton60_v7'                   , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton20NonIso_v0'                , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton20CaloIdL_v0'               , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton20CaloIsoM_v0'              , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton20CaloIdLCaloIsoM_v0'       , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton30_20_20NonIso_v0'          , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton30_20_20CaloIdLCaloIsoM_v0' , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton30_20_20CaloIdL_v0'         , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton30_20_20CaloIsoM_v0'        , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton40_40_10NonIso_v0'          , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton40_40_10CaloIdLCaloIsoM_v0' , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton40_40_10CaloIdL_v0'         , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton40_40_10CaloIsoM_v0'        , 'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu12_v0'                             , 'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu12_Photon25_CaloIdL_v8'            , 'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu12_DiPhoton20NonIso_v0'            , 'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu12_DiPhoton20CaloIdlLCaloIsoM_v0'  , 'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu12_DiPhoton20CaloIdlL_v0'          , 'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu12_DiPhoton20CaloIsoM_v0'          , 'L1Seeds' : [] },
]

triggers_80x = [

            {'trigger' : 'HLT_Photon22_v6'                         , 'L1Seeds' : [] },
            {'trigger' : 'HLT_SinglePhoton20NonIso_v0'             , 'L1Seeds' : [] },
            {'trigger' : 'HLT_SinglePhoton30NonIso_v0'             , 'L1Seeds' : [] },
            {'trigger' : 'HLT_SinglePhoton40NonIso_v0'             , 'L1Seeds' : [] },
            {'trigger' : 'HLT_DoublePhoton60_v7'                   , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton20NonIso_v0'                , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton30_20_20NonIso_v0'          , 'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton40_40_10NonIso_v0'          , 'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu12_Photon25_CaloIdL_v8'            , 'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu12_DiPhoton20NonIso_v0'            , 'L1Seeds' : [] },
]

triggers_new =  [
            {'trigger' : 'HLT_DoublePhoton70_v1'                                                     ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton302020NonIso_v0'                                              ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton404010NonIso_v0'                                              ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton35355NonIso_v0'                                               ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton302020NonIsoNoHE_v0'                                          ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton20NonIso_v0'                                                  ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton20CaloIdL_v0'                                                 ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton20CaloIsoM_v0'                                                ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton20CaloIdLCaloIsoM_v0'                                         ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_TriPhoton20NonIsoNoHE_v0'                                              ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_Photon33_v1'                                                           ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v7'                 ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_Diphoton30_22NonIso'                                                   ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_NoPixelVeto_Mass55_v7' ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_Photon50_R9Id90_HE10_IsoM_v9'                                          ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_TkMu17_v2'                                                             ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_TkMu27_v6'                                                             ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu27_v6'                                                               ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu12Diphoton20NonIso_v0'                                               ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu12Diphoton25_20NonIso_v0'                                            ,         'L1Seeds' : [] },
            {'trigger' : 'HLT_Mu12Diphoton30_25NonIso_v0'                                            ,         'L1Seeds' : [] },

]
_instlumi = 0.01  #pb-1/s
_TLS = 23.31

def main() :


    sampMan = SampleManager( options.baseDir, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    sampMan.ReadSamples( _MODULE )

    #makeDataRates(sampMan)

    makeMCRates(sampMan, key='')
    #makeMCRates(sampMan, key='EMEnriched')


def makeMCRates(sampMan, key) :

    all_results = OrderedDict()


    total_rates = []
    for trig in triggers_new : 

        trig_results = {}

        for samp in sampMan.get_samples() :
            if samp.name.count('QCD') == 0 : 
                continue

            if key :
                if samp.name.count( key ) == 0 :
                    continue
            else :
                if samp.name.count( 'EMEnriched' ) == 1 :
                    continue
            

            samp_info = {}

            sampMan.create_hist( samp.name, trig['trigger'] , '', (2, 0, 2) )

            x_sec = samp.cross_section

            n_evt  = samp.hist.Integral( )
            n_pass = samp.hist.GetBinContent( 2 )

            n_fail = n_evt - n_pass

            n_fail_f = ufloat( n_fail ,math.sqrt( n_fail ) )
            n_pass_f = ufloat( n_pass, math.sqrt( n_pass ) )

            print 'nevt = %d, npass = %d, frac = %f, xsec = %f '%( n_evt, n_pass, float(n_pass)/n_evt, x_sec )
            print 'rate = ', ( _instlumi * x_sec * n_pass_f / (n_pass_f+n_fail_f) ) 

            samp_info['nevt'] = n_pass_f + n_fail_f
            samp_info['npass'] = n_pass_f
            samp_info['nfail'] = n_fail_f
            samp_info['xsec'] = x_sec
            samp_info['eff_xs'] = x_sec * n_pass_f / (n_pass_f + n_fail_f )
            trig_results[samp.name] = samp_info
        
        total_rate = 0
        for name, data in trig_results.iteritems() :

            total_rate += data['eff_xs']

        total_rates.append( ( trig['trigger'], total_rate ) )

        all_results[trig['trigger']] = { 'total_rate' : total_rate*_instlumi, 'instlumi' : _instlumi, 'samp_info' : trig_results }

    for trig, total_rate in total_rates :

        print 'Trigger = %s' %(trig)
        print 'Rate = ', total_rate*_instlumi 

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )
        filename = 'rates_mc%s.pickle' %key
        ofile = open('%s/%s' %(options.outputDir, filename) , 'w')

        pickle.dump(all_results, ofile )

        ofile.close()




def makeDataRates(sampMan) :

    run_min, run_max = sampMan.get_sample_branch_minmax('Data','Run')
    lb_min, lb_max   = sampMan.get_sample_branch_minmax('Data','LumiBlock')

    print 'Run range = %d - %d ' %(run_min, run_max)
    print 'Lumi Block range = %d - %d ' %(lb_min, lb_max)

    sampMan.create_hist( 'Data', 'LumiBlock:Run', '', ( int(run_max-run_min+1), run_min, run_max+1, int(lb_max-lb_min+1), lb_min, lb_max+1 ) )

    run_vs_lb_hist = sampMan.get_samples(name='Data')[0].hist.Clone('run_vs_lb')

    n_ls = 0
    run_list = []
    for xbin in xrange( 1, run_vs_lb_hist.GetNbinsX() + 1 ) :
        for ybin in xrange( 1, run_vs_lb_hist.GetNbinsY() + 1 ) :
            cont = run_vs_lb_hist.GetBinContent( xbin, ybin )
            if cont > 0 :
                run_list.append( run_vs_lb_hist.GetXaxis().GetBinLowEdge( xbin ) )
                n_ls += 1

    run_list = list( set( run_list ) )


    print 'Data covers %d lumi sections' %n_ls
            
    print 'Data covers runs, '
    print run_list

    trig_counts = {}

    for trig in triggers_80x :

        print 'Get nPass for trigger ', trig['trigger']

        trig_counts[trig['trigger']] = 0

        sampMan.Draw( trig['trigger'], '', (2, 0, 2) )

        hist = sampMan.get_samples(name='Data')[0].hist.Clone( trig['trigger'] )

        npass = hist.GetBinContent(2)
        nfail = hist.GetBinContent(1)

        print 'npass = %d, nfail = %d' %( npass, nfail)

        print 'Rate for %s = %f' %( trig['trigger'], npass/ ( n_ls * _TLS ) )

main()
