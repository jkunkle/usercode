
from RooFitBase import fit_model_to_data, draw_fitted_results, SetHistContentBins
from SampleManager import SampleManager
from SampleManager import Sample
from uncertainties import ufloat
import uuid
import ROOT
import os
import pickle
import collections
from array import array

_photon_hist_eta_pt_bins = ( [0, 1.44, 1.57, 2.5], [15,20,25,30,40,50,70,100] )

uncert_base = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2015_06_05/SinglePhotonResults/SigmaIEIEFits/JetSinglePhotonFakeNomIso'
_photon_jet_fake_uncert_files = { 'mmg_eveto' : { 
                                   ('EB', '15', '20')  : uncert_base+'/results__muzpeak_tp_eveto__EB__pt_15-20.pickle',
                                   ('EB', '20', '25')  : uncert_base+'/results__muzpeak_tp_eveto__EB__pt_20-25.pickle',
                                   ('EB', '25', '30')  : uncert_base+'/results__muzpeak_tp_eveto__EB__pt_25-30.pickle',
                                   ('EB', '30', '40')  : uncert_base+'/results__muzpeak_tp_eveto__EB__pt_30-40.pickle',
                                   ('EB', '40', '50')  : uncert_base+'/results__muzpeak_tp_eveto__EB__pt_40-50.pickle',
                                   ('EE', '15', '20')  : uncert_base+'/results__muzpeak_tp_eveto__EE__pt_15-20.pickle',
                                   ('EE', '20', '25')  : uncert_base+'/results__muzpeak_tp_eveto__EE__pt_20-25.pickle',
                                   ('EE', '25', '30')  : uncert_base+'/results__muzpeak_tp_eveto__EE__pt_25-30.pickle',
                                   ('EE', '30', '40')  : uncert_base+'/results__muzpeak_tp_eveto__EE__pt_30-40.pickle',
                                   ('EE', '40', '50')  : uncert_base+'/results__muzpeak_tp_eveto__EE__pt_40-50.pickle',
                                   ('EB', '50', '70')  : uncert_base+'/results__muzpeak_tp_eveto__EB__pt_50-70.pickle',
                                   ('EE', '50', '70')  : uncert_base+'/results__muzpeak_tp_eveto__EE__pt_50-70.pickle',
                                 },
                                  'mg_eveto_highpt' : {
                                   ('EB', '70', 'max') : uncert_base+'/results__muw_tp_eveto__EB__pt_70-max.pickle',
                                   ('EE', '70', 'max') : uncert_base+'/results__muw_tp_eveto__EE__pt_70-max.pickle',
                                  },

                                  'mmg_medium' : {
                                   ('EB', '15', '20')  : uncert_base+'/results__muzpeak_tp_medium__EB__pt_15-20.pickle',
                                   ('EB', '20', '25')  : uncert_base+'/results__muzpeak_tp_medium__EB__pt_20-25.pickle',
                                   ('EB', '25', '30')  : uncert_base+'/results__muzpeak_tp_medium__EB__pt_25-30.pickle',
                                   ('EB', '30', '40')  : uncert_base+'/results__muzpeak_tp_medium__EB__pt_30-40.pickle',
                                   ('EB', '40', '50')  : uncert_base+'/results__muzpeak_tp_medium__EB__pt_40-50.pickle',
                                   ('EE', '15', '20')  : uncert_base+'/results__muzpeak_tp_medium__EE__pt_15-20.pickle',
                                   ('EE', '20', '25')  : uncert_base+'/results__muzpeak_tp_medium__EE__pt_20-25.pickle',
                                   ('EE', '25', '30')  : uncert_base+'/results__muzpeak_tp_medium__EE__pt_25-30.pickle',
                                   ('EE', '30', '40')  : uncert_base+'/results__muzpeak_tp_medium__EE__pt_30-40.pickle',
                                   ('EE', '40', '50')  : uncert_base+'/results__muzpeak_tp_medium__EE__pt_40-50.pickle',
                                   ('EB', '50', '70')  : uncert_base+'/results__muzpeak_tp_medium__EB__pt_50-70.pickle',
                                   ('EE', '50', '70')  : uncert_base+'/results__muzpeak_tp_medium__EE__pt_50-70.pickle',
                                  },
                                  'mg_medium_highpt' : {
                                   ('EB', '70', 'max') : uncert_base+'/results__muw_tp_medium__EB__pt_70-max.pickle',
                                   ('EE', '70', 'max') : uncert_base+'/results__muw_tp_medium__EE__pt_70-max.pickle',
                                  },

}


def get_default_draw_commands( ch ) :

    if ch=='mmg_medium' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_mediumNoEleVeto_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 15 && m_leplep < 80'
    elif ch=='mmg_eveto' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_medium_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 15 && m_leplep < 80'
    elif ch=='mg_medium_highpt' :
        return 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==1 && dr_ph1_leadLep>0.4 && mt_lep_met > 60'
    elif ch=='mg_eveto_highpt' :
        return 'mu_passtrig25_n>0 && mu_n==1 && ph_medium_n==1 && dr_ph1_leadLep>0.4 && mt_lep_met > 60'
    else :
        return None

def get_background_draw_commands( ch ) :

    if   ch=='mmg_medium' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_mediumNoEleVeto_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 81 && m_leplep < 101'
    elif ch=='mmg_eveto' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_medium_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 81 && m_leplep < 101'
    else :
        return None

def get_normalization_draw_commands_in( ch ) :

    if   ch=='mmg_medium' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 81 && m_leplep < 101'
    elif ch=='mmg_eveto' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && ph_hasPixSeed[0]==0 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 81 && m_leplep < 101'
    else :
        return None

def get_normalization_draw_commands_out( ch ) :

    if   ch=='mmg_medium' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep < 80 && m_leplep > 15 && m_leplepph > 76 && m_leplepph < 106'
    elif ch=='mmg_eveto' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && ph_hasPixSeed[0]==0 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep < 80 && m_leplep > 15 && m_leplepph > 76 && m_leplepph < 106'
    else :
        return None

def main() :

    # Parse command-line options
    from argparse import ArgumentParser
    p = ArgumentParser()
    
    p.add_argument('--outputDir',default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
    
    options = p.parse_args()
    
    if options.outputDir is not None :
        ROOT.gROOT.SetBatch(True)
    else :
        ROOT.gROOT.SetBatch(False)

    global sampManMMG
    global sampManMG

    base_dir_mmg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_04_11'
    base_dir_mg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_04_11'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'
    xsFile = 'cross_sections/wgamgam.py'
    lumi = 19400

    sampManMMG = SampleManager(base_dir_mmg, treeName=treename,filename=filename, xsFile=xsFile, lumi=lumi)
    sampManMG = SampleManager(base_dir_mg, treeName=treename,filename=filename, xsFile=xsFile, lumi=lumi)

    samplesConf = 'Modules/TAndPSampleConf.py'

    sampManMMG.ReadSamples( samplesConf )
    sampManMG.ReadSamples( samplesConf )

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )
        

        subdir = 'PhotonEfficiencies'
        outputDir = options.outputDir + '/' + subdir

        pt_bins = [15, 20, 25, 30, 40, 50, 70]

        #eff_medium_data = GetPhotonEfficiencies( data_sample='Muon'  , numerator = 'mmg_medium', denominator='mmg_loose' , pt_bins=pt_bins, bkg_sample='DYJetsToLLPhOlap', outputDir=outputDir+'/DataLLCut' )
        eff_eveto_data  = GetPhotonEfficiencies( data_sample='Muon'  , numerator = 'mmg_eveto' , denominator='mmg_medium', pt_bins=pt_bins, bkg_sample='DYJetsToLLPhOlap', outputDir=outputDir+'/DataLLCut' )
        #eff_medium_mc   = GetPhotonEfficiencies( data_sample='Zgamma', numerator = 'mmg_medium', denominator='mmg_loose' , pt_bins=pt_bins, bkg_sample=None, outputDir=outputDir+'/MCLLCut' )
        eff_eveto_mc    = GetPhotonEfficiencies( data_sample='Zgamma', numerator = 'mmg_eveto' , denominator='mmg_medium', pt_bins=pt_bins, bkg_sample=None, outputDir=outputDir+'/MCLLCut' )

        pt_bins_high = [70]

        #eff_medium_data = GetPhotonEfficienciesHighPt( data_sample='Muon'  , numerator='mmg_medium', denominator='mmg_loose' , pt_min=pt_min_high, outputDir=outputDir+'/DataLLCut' )
        eff_eveto_data_highpt  = GetPhotonEfficienciesHighPt( data_sample='Muon'  , numerator='mg_eveto_highpt' , denominator='mg_medium_highpt', ptbins=pt_bins_high, useBkgEstimate=True, outputDir=outputDir+'/DataLLCut' )
        #eff_medium_mc   = GetPhotonEfficienciesHighPt( data_sample='Zgamma', numerator='mmg_medium', denominator='mmg_loose' , pt_min=pt_min_high, outputDir=outputDir+'/MCLLCut' )
        eff_eveto_mc_highpt    = GetPhotonEfficienciesHighPt( data_sample='Wgamma', numerator='mg_eveto_highpt' , denominator='mg_medium_highpt', ptbins=pt_bins_high, useBkgEstimate=False, outputDir=outputDir+'/MCLLCut' )

        for bin, eff in eff_eveto_data_highpt.iteritems() :
            eff_eveto_data[bin] = eff
        for bin, eff in eff_eveto_mc_highpt.iteritems() :
            eff_eveto_mc[bin] = eff

        print 'Eveto data '
        for bin, eff in eff_eveto_data.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'Eveto MC '
        for bin, eff in eff_eveto_mc.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        #MakeScaleFactor( eff_medium_data, eff_medium_mc, tag='sf_medium_nom' , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )
        MakeScaleFactor( eff_eveto_data , eff_eveto_mc , tag='sf_eveto_nom'  , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )
        #MakeScaleFactor( eff_eveto_data_highpt , eff_eveto_mc_highpt , tag='sf_eveto_highpt'  , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )
        #MakeScaleFactor( eff_medium_data_llcut, eff_medium_mc_llcut, tag='sf_medium_llcut' , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )
        #MakeScaleFactor( eff_eveto_data_llcut , eff_eveto_mc_llcut , tag='sf_eveto_llcut'  , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )

def GetPhotonEfficienciesHighPt( data_sample, numerator, denominator, ptbins=[], useBkgEstimate=False,  outputDir=None ) :

    eta_reg = ['EB', 'EE']

    data_samp = sampManMMG.get_samples(name=data_sample )

    results = {}

    for reg in eta_reg :

        if reg == 'EB' :
            etamin = 0.0
            etamax = 1.44
        if reg == 'EE' :
            etamin = 1.57
            etamax = 2.50

        for idx, minpt in enumerate( ptbins ) :
            if idx == (len(ptbins)-1) :
                maxpt = 'max'
                ptstr = '%d-max' %minpt
            else :
                maxpt = ptbins[idx+1]
                ptstr = '%d-%d' %(minpt, maxpt)

            label_num = 'hist_num_%s_%s_%s' %( numerator, reg, ptstr)
            label_den = 'hist_den_%s_%s_%s' %( denominator, reg, ptstr)

            bin = ( str(etamin), str(etamax), str(minpt), str(maxpt) )

            # ----------------------------
            # Numerator
            # ----------------------------

            eff_num = GetEfficiencyIntegralsHighPt( data_sample=data_sample, draw_tag=numerator, label=label_num, eta_reg=reg, minpt=minpt, maxpt=maxpt, useBkgEstimate=useBkgEstimate)
            eff_den = GetEfficiencyIntegralsHighPt( data_sample=data_sample, draw_tag=denominator, label=label_den, eta_reg=reg, minpt=minpt, maxpt=maxpt, useBkgEstimate=useBkgEstimate)

            results[bin] = {}
            results[bin]['num'] = eff_num
            results[bin]['den'] = eff_den
            results[bin]['eff'] = eff_num['result']/eff_den['result']

    return results


def GetPhotonEfficiencies( data_sample, numerator, denominator, pt_bins=[], bkg_sample=None,  outputDir=None ) :

    eta_reg = ['EB', 'EE']

    data_samp = sampManMMG.get_samples(name=data_sample )

    results = {}

    for reg in eta_reg :

        if reg == 'EB' :
            etamin = 0.0
            etamax = 1.44
        if reg == 'EE' :
            etamin = 1.57
            etamax = 2.50

        for idx, minpt in enumerate( pt_bins[:-1] ) :
            maxpt = pt_bins[idx+1]

            bin = ( str(etamin), str(etamax), str( minpt ), str( maxpt ) )

            label_num = 'hist_num_%s_%s_%d-%d' %( numerator, reg, minpt, maxpt )
            label_den = 'hist_den_%s_%s_%d-%d' %( denominator, reg, minpt, maxpt )

            # ----------------------------
            # Numerator
            # ----------------------------

            eff_num = GetEfficiencyIntegrals( data_sample=data_sample, draw_tag=numerator, label=label_num, eta_reg=reg, minpt=minpt, maxpt=maxpt, bkg_sample=bkg_sample )
            eff_den = GetEfficiencyIntegrals( data_sample=data_sample, draw_tag=denominator, label=label_den, eta_reg=reg, minpt=minpt, maxpt=maxpt, bkg_sample=bkg_sample )

            results[bin] = {}
            results[bin]['num'] = eff_num
            results[bin]['den'] = eff_den
            results[bin]['eff'] = eff_num['result']/eff_den['result']

    return results


def GetEfficiencyIntegrals( data_sample, draw_tag, label, eta_reg, minpt, maxpt, bkg_sample=None ) :

    mass_binning = (200, 0, 200 )

    data_samp = sampManMMG.get_samples(name=data_sample )

    draw_base = get_default_draw_commands( draw_tag )
    draw_full = '%s && ph_Is%s[0] && ph_pt[0] > %d && ph_pt[0] < %d ' %( draw_base, eta_reg, minpt, maxpt )

    hist_data = clone_sample_and_draw( sampManMMG, data_samp[0], 'm_leplepph', 'PUWeight * ( %s )' %draw_full, mass_binning )
    hist_data.SetName( label+'_data' )

    err_data = ROOT.Double()
    int_data = hist_data.IntegralAndError( hist_data.FindBin( 76 ), hist_data.FindBin( 106 ), err_data )

    if bkg_sample is not None :

        bkg_samp = sampManMMG.get_samples( name=bkg_sample )

        draw_base_bkg_in = get_background_draw_commands( draw_tag )

        draw_full_bkg_in = '%s && ph_Is%s[0] && ph_pt[0] > %d && ph_pt[0] < %d ' %( draw_base_bkg_in, eta_reg, minpt, maxpt )

        hist_bkg_in = clone_sample_and_draw( sampManMMG, bkg_samp[0], 'm_leplep', 'PUWeight * ( %s )' %draw_full_bkg_in, mass_binning )
        hist_bkg_in.SetName( label+'_bkgIN' )

        err_bkg_in = ROOT.Double()
        int_bkg_in = hist_bkg_in.IntegralAndError( hist_bkg_in.FindBin( 81 ), hist_bkg_in.FindBin( 101 ), err_bkg_in )

        # get background estimate from
        # data driven jet fake
        dd_file = _photon_jet_fake_uncert_files[draw_tag][(eta_reg, str(minpt), str(maxpt))]

        dd_ofile = open( dd_file, 'r')
        dd_data = pickle.load( dd_ofile )
        dd_val = dd_data['Npred_F_T']

        # now get the integrals from the in and out regions with loose photon selection
        #IN
        draw_base_loose_in = get_normalization_draw_commands_in( draw_tag )
        draw_full_loose_in = '%s && ph_Is%s[0] && ph_pt[0] > %d && ph_pt[0] < %d ' %( draw_base_loose_in, eta_reg, minpt, maxpt )

        hist_loose_in = clone_sample_and_draw( sampManMMG, bkg_samp[0], 'm_leplep', 'PUWeight * ( %s )' %draw_full_loose_in, mass_binning )
        hist_loose_in.SetName( label+'_looseIN' )

        err_loose_in = ROOT.Double()
        int_loose_in = hist_loose_in.IntegralAndError( hist_loose_in.FindBin( 81 ), hist_loose_in.FindBin(101), err_loose_in )

        #OUT
        draw_base_loose_out = get_normalization_draw_commands_out( draw_tag )
        draw_full_loose_out = '%s && ph_Is%s[0] && ph_pt[0] > %d && ph_pt[0] < %d ' %( draw_base_loose_out, eta_reg, minpt, maxpt )

        hist_loose_out = clone_sample_and_draw( sampManMMG, bkg_samp[0], 'm_leplepph', 'PUWeight * ( %s )' %draw_full_loose_out, mass_binning )
        hist_loose_out.SetName( label+'_looseIN' )

        err_loose_out = ROOT.Double()
        int_loose_out = hist_loose_out.IntegralAndError( hist_loose_out.FindBin( 76 ), hist_loose_out.FindBin(106), err_loose_out )

        # now make the ufloats and do the division
        val_loose_in = ufloat( int_loose_in, err_loose_in )
        val_loose_out = ufloat( int_loose_out, err_loose_out )
        val_bkg_in = ufloat( int_bkg_in, err_bkg_in )
        val_data = ufloat( int_data, err_data )

        results = {}
        results = {}
        results['%s_loose_in' %bkg_sample] = val_loose_in
        results['%s_loose_out' %bkg_sample] = val_loose_out
        results['%s_bkg_in' %bkg_sample] = val_bkg_in
        results['Data' ] = val_data
        results['JetFakeBkg' ] = dd_val


        loose_in_out_ratio = (val_loose_out/val_loose_in)
        dd_extrap_bkg      = dd_val*loose_in_out_ratio

        results['loose_in_out_ratio'] = loose_in_out_ratio
        results['Bkg_pred'] = dd_extrap_bkg
        results['result'] = val_data - dd_extrap_bkg

        return results

    else :

        # just take the number from data
        val_data = ufloat( int_data, err_data )
        results = {}
        results['result'] = val_data
        return results

def GetEfficiencyIntegralsHighPt( data_sample, draw_tag, label, eta_reg, minpt, maxpt='max', useBkgEstimate=False ) :

    mass_binning = (200, 0, 200 )

    data_samp = sampManMG.get_samples(name=data_sample )

    draw_base = get_default_draw_commands( draw_tag )
    draw_full = '%s && ph_Is%s[0] && ph_pt[0] > %d ' %( draw_base, eta_reg, minpt )
    if maxpt != 'max' :
        draw_full += ' && ph_pt[0] < %d' %maxpt

    hist_data = clone_sample_and_draw( sampManMG, data_samp[0], 'mt_lep_met', 'PUWeight * ( %s )' %draw_full, mass_binning )
    hist_data.SetName( label+'_data' )

    err_data = ROOT.Double()
    int_data = hist_data.IntegralAndError(  1, hist_data.GetNbinsX(), err_data )

    reg_bin = ( eta_reg, str(minpt), str(maxpt))

    if useBkgEstimate :

        # get background estimate from
        # data driven jet fake
        dd_file = _photon_jet_fake_uncert_files[draw_tag][reg_bin]

        dd_ofile = open( dd_file, 'r')
        dd_data = pickle.load( dd_ofile )
        dd_val = dd_data['Npred_F_T']

        val_data = ufloat( int_data, err_data )

        results = {}
        results = {}
        results['Data' ] = val_data
        results['JetFakeBkg' ] = dd_val
        results['result'] = val_data - dd_val

        print results

        return results

    else :

        # just take the number from data
        val_data = ufloat( int_data, err_data )
        results = {}
        results['result'] = val_data
        return results

def MakeScaleFactor( numerator, denominator, tag, binning, outputDir=None ) :
    

    # numerator is data, denominator is MC
    scale_factors = {}
    for bin, res_num in numerator.iteritems() :

        if bin not in denominator :
            print 'Bin not found in denominator', bin
            print numerator
            print denominator
            continue

        res_den = denominator[bin]

        if res_den == 0 :
            print 'SF denominator is zero!'
            scale_factors[bin] = 1000000
        else :
            scale_factors[bin] = res_num['eff'] / res_den['eff']


    hist_sf = ROOT.TH2F( 'hist_%s' %tag, 'hist_%s' %tag, len(binning[0])-1, array( 'f', binning[0]), len(binning[1])-1, array('f', binning[1]) )

    print 'GOt Scale factor'
    print scale_factors

    for bin, sf in scale_factors.iteritems() : 

        etamin = float( bin[0] )
        etamax = float( bin[1] )
        ptmin  = float( bin[2] )
        if bin[3] == 'max' : 
            ptmax = hist_sf.GetYaxis().GetBinUpEdge( hist_sf.GetNbinsY() )
        else :
            ptmax  = float( bin[3] )

        SetHistContentBins( hist_sf, sf, etamin, etamax, ptmin, ptmax )


    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )
        file_sf = ROOT.TFile.Open( '%s/hist_%s.root' %( outputDir, tag ), 'RECREATE' )
        print 'Write root file ', file_sf.GetName()
        hist_sf.Write()
        file_sf.Close()

        file_pick = open( '%s/results_%s.pickle' %(outputDir, tag), 'w' )
        pickle.dump( scale_factors, file_pick )
        file_pick.close()

        file_num = open( '%s/details_data_%s.pickle' %(outputDir, tag), 'w' )
        pickle.dump( numerator, file_num )
        file_num.close()

        file_den = open( '%s/details_mc_%s.pickle' %(outputDir, tag), 'w' )
        pickle.dump( denominator, file_den )
        file_den.close()

def pair_pt_eta_bins( bin_list ) :

    paired_bins = {}

    for ptbins, etabins in bin_list :
        paired_eta = []
        for etaidx, etamin in enumerate(etabins[:-1]) :
            etamax = etabins[etaidx+1]
            paired_eta.append( ( etamin, etamax ) )

        for ptidx, ptmin in enumerate(ptbins[:-1]) :
            ptmax = ptbins[ptidx+1]
            paired_bins[ (ptmin, ptmax) ] = paired_eta

    return paired_bins


def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :
        newSamp = sampMan.clone_sample( oldname=samp.name, newname=samp.name+str(uuid.uuid4()), temporary=True ) 
        sampMan.create_hist( newSamp, var, sel, binning )
        return newSamp.hist
                                       
if __name__ == '__main__' :
    main()
