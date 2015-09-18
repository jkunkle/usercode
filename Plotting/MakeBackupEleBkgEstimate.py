import pickle
import os
from uncertainties import ufloat
from SampleManager import SampleManager
from MakeBackgroundEstimates import get_dirs_and_files, get_mapped_directory, save_hist, add_syst_to_hist


from argparse import ArgumentParser

p = ArgumentParser()

p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',  required=True,       help='Input directory base')

options = p.parse_args()

lead_dr_cut = 0.4

draw_str = {
    'inv' : 'el_passtrig_n>0 && ph_mediumFailEleVeto_n==1 && ph_hasPixSeed[0]==1 && m_trigelph1 > 76 && m_trigelph1 < 106 ',
    'nom' : 'el_passtrig_n>0 && ph_medium_n==1 && ph_hasPixSeed[0]==0  && m_trigelph1 > 76 && m_trigelph1 < 106 ',
}

_regions = ['EB', 'EE']

def main() :

    global samplesLGPass
    global samplesLGFail

    baseDirLGPass   = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaMediumPhIDPassPixSeed_2015_09_14'
    baseDirLGFail   = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaMediumPhIDFailPixSeed_2015_09_14'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConf = 'Modules/ElectronFake.py'

    samplesLGPass   = SampleManager(baseDirLGPass ,  treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesLGFail   = SampleManager(baseDirLGFail ,  treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)

    samplesLGPass  .ReadSamples( sampleConf )
    samplesLGFail  .ReadSamples( sampleConf )

    #eta_bins = {'EB' : [(0.00, 0.10), (0.10, 0.50), (0.50, 1.00), (1.00, 1.44)],
    #            'EE' : [(1.57, 2.10), (2.10, 2.20), (2.20, 2.40), (2.40, 2.50)]}

    eta_bins = {'EB' : [(0.00, 1.44)],
                'EE' : [(1.57, 2.50)]}

    #pt_bins = [(15, 25), (25, 40), (40, 70), (70,1000000) ]
    pt_bins = [15, 25, 40, 70,1000000]

    base_dir_jet_single = '%s/SinglePhotonResults/SigmaIEIEFits' %(options.baseDir)

    jet_fake_nom = MakeSingleJetBkgEstimate( base_dir_jet_single, channel='elwzcr',pt_bins=pt_bins, eta_bins={})
    jet_fake_inv = MakeSingleJetBkgEstimate( base_dir_jet_single, channel='elwzcrinvpixlead',pt_bins=pt_bins, eta_bins={})
    #jet_fake_nom = MakeSingleJetBkgEstimate( base_dir_jet_single, channel='elwzcrloose',pt_bins=pt_bins, eta_bins={})
    #jet_fake_inv = MakeSingleJetBkgEstimate( base_dir_jet_single, channel='elwzcrlooseinvpixlead',pt_bins=pt_bins, eta_bins={})

    print jet_fake_nom

    output_dir = '%s/ElectronFakeManualLoose' %options.baseDir

    MakeEleBkgEstimate( output_dir, jet_fake_nom, jet_fake_inv, pt_bins, mc_bkgs=['Wgamma', 'Zgamma'] )

    print '^_^ FINISHED! ^_^'

def MakeEleBkgEstimate( output_dir, jet_fake_nom, jet_fake_inv, pt_bins, eta_bins={}, mc_bkgs = [] ) :

    samplesLGPass.deactivate_all_samples()
    samplesLGFail.deactivate_all_samples()
    for bkg in mc_bkgs :
        samplesLGPass.activate_sample( bkg )
        samplesLGFail.activate_sample( bkg )

    samplesLGPass.activate_sample( 'Electron' )
    samplesLGFail.activate_sample( 'Electron' )

    var = 'ph_pt[0]'
    data_inv = get_hist_data( var, pt_bins, jet_fake_inv, mc_bkgs, _regions, 'inv' )
    data_nom = get_hist_data( var, pt_bins, jet_fake_nom, mc_bkgs, _regions, 'nom' )

    print data_inv
    print data_nom

    result_dic = {}
    result_dic['fake_ratio'] = {}

    eta_bins = { 'EB' : ('0.00', '1.44'), 'EE' : ('1.57' , '2.50') }

    subl_pt_bins = { (15, 40) : [(15,25),(25,40) ], 
                    (15, 70) :  [(15,25),(25,40),(40,70) ],
                     (15, 1000000) : [(15,25),(25,40),(40,70), (70, 1000000) ],
                   }

    for resbin, dataval_nom in data_nom['data'].iteritems() :

        bkgval_nom = data_nom['background'][resbin]

        dataval_inv = data_inv['data'][resbin]
        bkgval_inv  = data_inv['background'][resbin]

        output_bin = ( str( resbin[1]), str(resbin[2]), eta_bins[resbin[0]][0], eta_bins[resbin[0]][1] )

        #result_dic['fake_ratio'][output_bin] = ( dataval_nom - bkgval_nom ) / ( dataval_inv - bkgval_inv )
        result_dic['fake_ratio'][output_bin] = ( dataval_nom - bkgval_nom ) / ( dataval_inv - bkgval_inv )

    for eta in eta_bins.keys() :
        for subl_range, pt_bins in subl_pt_bins.iteritems() :

            subldata_nom = 0.0
            sublbkg_nom  = 0.0
            subldata_inv = 0.0
            sublbkg_inv  = 0.0

            for resbin, dataval_nom in data_nom['data'].iteritems() :

                if resbin[0] == eta :
                    if ( resbin[1], resbin[2]) in pt_bins :

                        bkgval_nom = data_nom['background'][resbin]

                        dataval_inv = data_inv['data'][resbin]
                        bkgval_inv  = data_inv['background'][resbin]

                        subldata_nom += dataval_nom
                        subldata_inv += dataval_inv

                        sublbkg_nom += bkgval_nom
                        sublbkg_inv += bkgval_inv

            output_bin = ( str( subl_range[0]), str(subl_range[1]), eta_bins[eta][0], eta_bins[eta][1] )
            result_dic['fake_ratio'][output_bin] = ( subldata_nom - sublbkg_nom ) / ( subldata_inv - sublbkg_inv )


    if not os.path.isdir( output_dir ) :
        os.makedirs( output_dir )

    print result_dic
    output_file = '%s/results.pickle' %( output_dir )

    ofile = open( output_file, 'w') 
    pickle.dump( result_dic, ofile )

    ofile.close()


def get_hist_data( var, pt_bins, jet_fake,mc_bkgs, regions, tag ) :


    results = {}
    results['data'] = {}
    results['background'] = {}

    if tag not in ['inv', 'nom'] :
        print 'incorrect tag'
        return results

    for reg in regions :

        selection= ' PUWeight * ( %s && ph_Is%s[0]  ) ' %(draw_str[tag], reg)


        if tag == 'nom' :
            samplesLG = samplesLGPass
        elif tag == 'inv' :
            samplesLG = samplesLGFail

        samplesLG.Draw( var, selection, pt_bins)

        hist_data = samplesLG.get_samples(name='Electron')[0].hist.Clone('Data_%s' %tag)

        hist_bkg_mc = None
        for bkg in mc_bkgs :
            if hist_bkg_mc is None :
                hist_bkg_mc = samplesLG.get_samples( name=bkg )[0].hist.Clone( 'Background_%s' %tag)
            else :
                hist_bkg_mc.Add( samplesLG.get_samples( name=bkg )[0].hist )

        
        for idx, ptmin in enumerate( pt_bins[:-1] ) :
            ptmax = pt_bins[idx+1]

            ptminstr = str(ptmin)
            ptmaxstr = str(ptmax)
            if ptmax == pt_bins[-1] :
                ptmaxstr = 'max'

            hist_bin = hist_data.FindBin( ptmin )

            print 'Ptmin = %d, hist_bin = %d' %( ptmin, hist_bin )

            data_val   = hist_data.GetBinContent(hist_bin)
            data_err   = hist_data.GetBinError(hist_bin)
            mc_bkg_val = hist_bkg_mc.GetBinContent(hist_bin)
            mc_bkg_err = hist_bkg_mc.GetBinError(hist_bin)

            data = ufloat( data_val, data_err )
            mc_bkg = ufloat( mc_bkg_val, mc_bkg_err )


            jet_bin = ( reg, ptminstr, ptmaxstr )
            jet_bkg = jet_fake['stat+syst']['f'][jet_bin]

            res_bin = ( reg, ptmin, ptmax )

            results['data'][res_bin] = data
            results['background'][res_bin] = mc_bkg+jet_bkg

    return results






def MakeSingleJetBkgEstimate( base_dir_jet, channel='', pt_bins=[],eta_bins={}, outputDir=None ) :

    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

    regions = ['EB', 'EE']

    # get the pt bins in the format expected
    # in the pickle files
    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
    pt_bins_jetfile.append( 'max')

    # regex expression to match directories
    # where jet fake results should be found
    # if the Corr directories are used 
    # it will prioritize to the minimum values
    jet_dirs_key = 'JetSinglePhotonFakeNomIso'
    #jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'

    # get the directories mapped to the integer values matched
    # if no values are matched the directory is matched ot (0,0,0)
    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )

    file_key_eta = 'results__%s__(\d\.\d\d-\d\.\d\d)__pt_(\d+)-(\d+|max).pickle' %channel
    file_key_eta_syst = 'results__syst__%s__(\d\.\d\d-\d\.\d\d)__pt_(\d+)-(\d+|max).pickle' %channel
    file_key = 'results__%s__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %channel
    file_key_syst = 'results__syst__%s__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %channel

    #jet_files_eta      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_eta      )
    #jet_files_eta_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_eta_syst )
    jet_files      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key      )
    jet_files_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_syst )

    #update_jet_files_dict( jet_files, jet_files_eta )
    #update_jet_files_dict( jet_files_syst, jet_files_eta_syst )

    jet_pred     = get_jet_single_fake_results( jet_files    , jet_files_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet, eta_bins=eta_bins ) 

    print 'Predicted Jet fakes for channel %s' %channel

    for r1 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
            ptmax = pt_bins_jetfile[idx+1]

            if eta_bins :
                for etamin, etamax in eta_bins[r1] :

                    bin = ('%.2f-%.2f'%(etamin,etamax), ptmin, ptmax)

                    print 'Region %s, pt %s-%s' %( bin[0],ptmin,ptmax)
                    print 'Predicted Stat r = %s, predicted f = %s' %( jet_pred['stat']['r'][bin], jet_pred['stat']['f'][bin] ) 
                    print 'Predicted Syst r = %s, predicted f = %s' %( jet_pred['syst']['r'][bin], jet_pred['syst']['f'][bin] )
                    print 'Predicted Stat+Syst r = %s, predicted f = %s' %( jet_pred['stat+syst']['r'][bin], jet_pred['stat+syst']['f'][bin] )
            else :
                bin = (r1,ptmin,ptmax)

                print 'Region %s, pt %s-%s' %( r1,ptmin,ptmax)
                print 'Predicted Stat r = %s, predicted f = %s' %( jet_pred['stat']['r'][bin], jet_pred['stat']['f'][bin] ) 
                print 'Predicted Syst r = %s, predicted f = %s' %( jet_pred['syst']['r'][bin], jet_pred['syst']['f'][bin] )
                print 'Predicted Stat+Syst r = %s, predicted f = %s' %( jet_pred['stat+syst']['r'][bin], jet_pred['stat+syst']['f'][bin] )



    return jet_pred


def get_jet_single_fake_results( jet_files, jet_files_syst, regions, pt_bins, jet_dir_key_map, base_dir_jet, eta_bins={} ) :
    """ Get the fake results for all pt and eta regions 
    
        Check if the data counts that were input to the 
        fit are non-zero.  If so, move to a looser isolation.
        If the values are never set, ie even in the loosest
        case there are no data counts, then use the 
        original with zero values
    """
    sorted_jet_dirs = jet_files.keys()
    sorted_jet_dirs.sort()

    results = {'stat' : {}, 'syst' : {}, 'stat+syst' : {} }
    for val in results.values() :
       val['f'] = {}
       val['r'] = {}
       val['result'] = {}

    for r1 in regions :

        for idx, ptmin in enumerate(pt_bins[:-1]) :
            ptmax = pt_bins[idx+1]

            if eta_bins :
                for etamin, etamax in eta_bins[r1] :
                    reg_bin = ('%.2f-%.2f' %(etamin,etamax), ptmin, ptmax)

                    get_jet_fake_results_from_file( results, reg_bin, base_dir_jet, sorted_jet_dirs, jet_dir_key_map, jet_files, jet_files_syst, region='%s_%s-%s' %(reg_bin[0], ptmin, ptmax))
                reg_bin = (r1, ptmin, ptmax) 

                get_jet_fake_results_from_file( results, reg_bin, base_dir_jet, sorted_jet_dirs, jet_dir_key_map, jet_files, jet_files_syst, region='%s_%s-%s' %(r1, ptmin, ptmax))
            else :

                reg_bin = (r1, ptmin, ptmax) 

                get_jet_fake_results_from_file( results, reg_bin, base_dir_jet, sorted_jet_dirs, jet_dir_key_map, jet_files, jet_files_syst, region='%s_%s-%s' %(r1, ptmin, ptmax))

    return results

def get_jet_fake_results_from_file( results, reg_bin, base_dir_jet, sorted_jet_dirs, jet_dir_key_map, jet_files, jet_files_syst, region='' ) :

    for val in results.values() :
        val['r'][reg_bin] = None
        val['f'][reg_bin] = None
        val['result'][reg_bin] = None

    for dir_key in sorted_jet_dirs :
        
        fentries = jet_files[dir_key]
        fentries_syst = jet_files_syst[dir_key]

        sub_dir_jet = jet_dir_key_map[dir_key]

        ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries[reg_bin])
        predictions = pickle.load(ofile)
        ofile.close()

        ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin])
        predictions_syst = pickle.load(ofile)
        ofile.close()

        Ndata_t = predictions['Ndata_T']
        Ndata_l = predictions['Ndata_L']

        if Ndata_t == 0 or Ndata_l == 0 :
            print 'No data entries for AsymIso %d-%d-%d, region %s ' %( dir_key[0], dir_key[1], dir_key[2], region  )
            print 'Ndata_t = %s, Ndata_l = %s' %( Ndata_t, Ndata_l)
            continue

        Npred_f = predictions['Npred_F_T']
        Npred_r = predictions['Npred_R_T']

        Npred_r_syst = predictions_syst['Npred_R_T']
        Npred_f_syst = predictions_syst['Npred_F_T']

        results['stat']['r'][reg_bin] = Npred_r
        results['stat']['f'][reg_bin] = Npred_f
        results['stat']['result'][reg_bin] = Npred_f

        results['syst']['r'][reg_bin] = Npred_r_syst
        results['syst']['f'][reg_bin] = Npred_f_syst
        results['syst']['result'][reg_bin] = Npred_f_syst

        Npred_r_tot = Npred_r
        Npred_f_tot = Npred_f

        Npred_r_syst_zero =ufloat( 0, Npred_r_syst.s )
        Npred_f_syst_zero =ufloat( 0, Npred_f_syst.s )
        results['stat+syst']['r'][reg_bin] = Npred_r_tot
        results['stat+syst']['f'][reg_bin] = Npred_f_tot
        results['stat+syst']['result'][reg_bin] = Npred_f_tot

        break

    # if results weren't set in any cases above, 
    # get the results from the first entry
    if results['stat']['r'][reg_bin] is None or results['stat']['f'][reg_bin] is None :

        dir_key = sorted_jet_dirs[0]

        fentries = jet_files[dir_key]

        sub_dir_jet = jet_dir_key_map[dir_key]

        ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries[reg_bin])
        predictions = pickle.load(ofile)
        ofile.close()

        ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin])
        predictions_syst = pickle.load(ofile)
        ofile.close()

        Npred_r = predictions['Npred_R_T']
        Npred_f = predictions['Npred_F_T']

        Npred_r_syst = predictions_syst['Npred_R_T']
        Npred_f_syst = predictions_syst['Npred_F_T']

        results['stat']['r'][reg_bin] = Npred_r
        results['stat']['f'][reg_bin] = Npred_f
        results['stat']['result'][reg_bin] = Npred_f

        results['syst']['r'][reg_bin] = Npred_r_syst
        results['syst']['f'][reg_bin] = Npred_f_syst
        results['syst']['result'][reg_bin] = Npred_f_syst

        Npred_r_tot = Npred_r
        Npred_f_tot = Npred_f

        Npred_r_syst_zero =ufloat( 0, Npred_r_syst.s )
        Npred_f_syst_zero =ufloat( 0, Npred_f_syst.s )

        Npred_r_tot += Npred_r_syst_zero
        Npred_f_tot += Npred_f_syst_zero
        
        results['stat+syst']['r'][reg_bin] = Npred_r_tot
        results['stat+syst']['f'][reg_bin] = Npred_f_tot
        results['stat+syst']['result'][reg_bin] = Npred_f_tot


main()


