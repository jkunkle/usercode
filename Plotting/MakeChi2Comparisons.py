import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import uuid
import time
import math

from SampleManager import SampleManager
from argparse import ArgumentParser
parser = ArgumentParser()

parser = ArgumentParser()
parser.add_argument('--baseDir',      default=None,           dest='baseDir',         required=True, help='Path to base directory')
parser.add_argument('--samplesConf',  default=None,           dest='samplesConf',     required=True, help='Sample configuration' )

options = parser.parse_args()


_TREENAME = 'tupel/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36200

rand = ROOT.TRandom3()
rand.SetSeed( int( time.time() ) )

def main() :

    sampMan = SampleManager( options.baseDir, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    if options.samplesConf is not None :

        sampMan.ReadSamples( options.samplesConf )
    else :
        print 'Must provide a sample configuration.  Exiting'
        return


    doVarScaleComparison( sampMan )

    #doPhiCutComparison( sampMan )

def doPhiCutComparison( sampMan ) :

    signal = 'ResonanceMass400'
    background = 'MCBackground'
    selection = 'mu_n==1 && ph_pt[0] > 30  '

    nsteps = 20

    val_min = 0
    val_max = 3.15

    interval = (val_max - val_min )/ nsteps

    results = []
    for istep in xrange( 0, nsteps ) :

        thisval = val_min + interval*istep

        this_selection = selection + ' && fabs( dphi_lep_ph ) > %f' %thisval

        theta = math.atan(1./1.96)

        binning = range( 60, 600, 20 ) 

        res = MakeChi2Comparison( sampMan, var='ph_pt[0] *sin( %f ) + mt_lep_met_ph*cos(%f)' %(theta,theta), selection = this_selection, binning=binning,signal=signal, background=background, fit_min=60, fit_max=600, sig_min=1, sig_max = 1, nsteps = 1 )

        results.append( ( thisval, res[0][1] ) )

    print results

    graph_res = ROOT.TGraph( len(results) ) 

    for idx, (xval, yval) in enumerate(results) :
        graph_res.SetPoint( idx, xval, yval )

    graph_res.SetMarkerStyle(20)
    graph_res.Draw('AP')

    raw_input('cont')




def doVarScaleComparison( sampMan ) :


    signal = 'ResonanceMass400'
    background = 'MCBackground'
    selection = 'mu_n==1 && ph_pt[0] > 30 && fabs(dphi_lep_ph) > 1.5 && fabs(dphi_lep_met) < 1.5 '

    bin_width = 20
    binning = range( 60, 600, 20 ) 

    binning_pt = range( 50, 410, 10 )


    theta = math.atan(1./1.96)
    results_comb = MakeChi2Comparison( sampMan, var='ph_pt[0] *sin( %f ) + mt_lep_met_ph*cos(%f)' %(theta,theta), selection = selection, binning=binning,signal=signal, background=background, fit_min=60, fit_max=600, sig_min=0.01, sig_max = 100, nsteps = 1000 )
    results_pt = MakeChi2Comparison( sampMan, var='ph_pt[0]', selection = selection, signal=signal, background=background, binning=binning_pt, fit_min=50, fit_max=400, sig_min=0.01, sig_max = 100, nsteps = 1000 )
    results_mt = MakeChi2Comparison( sampMan, var='mt_lep_met_ph', selection = selection, signal=signal, background=background, binning=binning, fit_min=60, fit_max=600, sig_min=0.01, sig_max = 100, nsteps = 1000 )
    results_m_mt = MakeChi2Comparison( sampMan, var='ph_pt[0] *sin( %f ) + mt_res*cos(%f)' %(theta,theta), selection = selection, signal=signal, background=background, binning=binning, fit_min=60, fit_max=600, sig_min=0.01, sig_max = 100, nsteps = 1000 )

    graph_pt = ROOT.TGraph( len( results_pt ) )
    graph_pt.SetName( 'graph_pt' )
    graph_mt = ROOT.TGraph( len( results_mt ) )
    graph_mt.SetName( 'graph_mt' )
    graph_m_mt = ROOT.TGraph( len( results_m_mt ) )
    graph_m_mt.SetName( 'graph_m_mt' )
    graph_comb = ROOT.TGraph( len( results_comb ) )
    graph_comb.SetName( 'graph_comb' )

    for idx, point in enumerate(results_pt) :
        graph_pt.SetPoint( idx, point[0], point[1] )
    for idx, point in enumerate(results_mt) :
        graph_mt.SetPoint( idx, point[0], point[1] )
    for idx, point in enumerate(results_m_mt) :
        graph_m_mt.SetPoint( idx, point[0], point[1] )
    for idx, point in enumerate(results_comb) :
        graph_comb.SetPoint( idx, point[0], point[1] )

    graph_pt.SetLineColor( ROOT.kBlack)
    graph_pt.SetMarkerColor( ROOT.kBlack)
    graph_pt.SetMarkerStyle( 20 )

    graph_mt.SetLineColor( ROOT.kBlue)
    graph_mt.SetMarkerColor( ROOT.kBlue)
    graph_mt.SetMarkerStyle( 20 )

    graph_m_mt.SetLineColor( ROOT.kGreen)
    graph_m_mt.SetMarkerColor( ROOT.kGreen)
    graph_m_mt.SetMarkerStyle( 20 )

    graph_comb.SetLineColor( ROOT.kMagenta)
    graph_comb.SetMarkerColor( ROOT.kMagenta)
    graph_comb.SetMarkerStyle( 20 )

    graph_pt.Draw('AP')
    graph_mt.Draw('Psame')
    graph_m_mt.Draw('Psame')
    graph_comb.Draw('Psame')

    leg = ROOT.TLegend( 0.5, 0.5, 0.9, 0.9)
    leg.AddEntry( graph_pt  , 'pT'   )
    leg.AddEntry( graph_mt  , 'mT'   )
    leg.AddEntry( graph_m_mt, 'mT_res' )
    leg.AddEntry( graph_comb, 'Comb' )

    leg.Draw()

    raw_input('comb')

    # do phi comparison

def MakeChi2Comparison( sampMan, var, selection, binning, signal, background, fit_min, fit_max, sig_min, sig_max, nsteps ) :

    points = []

    full_selection = selection + ' && (%s) > %f && (%s) < %f' %( var, fit_min, var, fit_max )

    sampMan.create_hist( signal, var,full_selection, binning )
    sampMan.create_hist( background, var,full_selection, binning )

    sig_hist = sampMan.get_samples(name=signal)[0].hist.Clone( 'signal')
    bkg_hist = sampMan.get_samples(name=background)[0].hist.Clone( 'background')

    #x_var = ROOT.RooRealVar( var, var, fit_min, fit_max )
    
    #bkg_template_hist = ROOT.RooDataHist( 'bkg_template_hist', 'bkg_template_hist', ROOT.RooArgList( x_var ), bkg_hist)
    #bkg_template = ROOT.RooHistPdf( 'bkg_template', 'bkg_template', ROOT.RooArgSet( x_var ), bkg_template_hist )

    #sig_hist = sig_hist.Clone( 'sig_hist' )
    #sig_template_hist = ROOT.RooDataHist( 'sig_template_hist', 'sig_template_hist', ROOT.RooArgList( x_var ), sig_hist)
    #sig_template = ROOT.RooHistPdf( 'sig_template', 'sig_template', ROOT.RooArgSet( x_var ), sig_template_hist )

    #nsig = ROOT.RooRealVar('nsig', '#signal events'    , 1,0,1000000.)
    #nbkg = ROOT.RooRealVar('nbkg', '#background events'    , bkg_hist.Integral(),0,1000000.)

    data = bkg_hist.Clone( 'data' )
    #for ibin in range( 1, data.GetNbinsX()+1 ) :
    #    bin_val = data.GetBinContent( ibin )
    #    rand_val = rand.Poisson( bin_val )
    #    data.SetBinContent( ibin, rand_val )
    #    data.SetBinError( ibin, math.sqrt( rand_val ) )

    #data_hist = ROOT.RooDataHist( 'data_hist', 'data_hist', ROOT.RooArgList( x_var ), data)
    #data_pdf= ROOT.RooHistPdf( 'data_pdf', 'data_pdf', ROOT.RooArgSet( x_var ), data_hist )

    #chi2 = bkg_hist.Chi2Test( data , 'WWCHI2/NDF')
    chi2 = bkg_hist.Chi2Test( data , 'WWCHI2')

    #mychi2 = calc_chi_2( bkg_hist, data)

    initial_chi2 = chi2/(data.GetNbinsX() -1 )

    print 'Initial chi2 = ', initial_chi2

    divisor = 1.0 / sig_min

    if divisor > 1 :
        start = 1
    else :
        start = sig_min

    interval = ( sig_max - sig_min ) / nsteps
    drew_example = False
    for iscale in xrange( 0, nsteps ) :

        scale = sig_min + interval*iscale

        #sig_bkg_models = ROOT.TObjArray()
        #sig_bkg_models.Add( bkg_template )
        #sig_bkg_models.Add( sig_template )

        #sig_bkg_vars = ROOT.TObjArray()
        #sig_bkg_vars.Add( nbkg )
        #sig_bkg_vars.Add( nsig )

        #model = ROOT.RooAddPdf( str(uuid.uuid4()), 'model', ROOT.RooArgList( sig_bkg_models ), ROOT.RooArgList( sig_bkg_vars ) )
        #model.Print()
        #print 'integral = ', model.createIntegral(ROOT.RooArgSet(x_var)).getVal()

        #nsig.setVal( sig_hist.Integral() * scale )
        #nsig.setVal( sig_hist.Integral() )
        #nbkg.setVal( bkg_hist.Integral())

        model = bkg_hist.Clone( 'model_step%d' %iscale )
        sig = sig_hist.Clone( 'sig_step%d' %iscale )

        sig.Scale( scale )

        model.Add( sig )

        #model.Draw()
        #raw_input('cont')

        #chi2 = model.Chi2Test( data, 'WWCHI2/NDF' )
        chi2 = model.Chi2Test( data, 'WWCHI2' )
        
        #chi2 = model.createChi2( data_hist )
        this_chi2 = chi2/(data.GetNbinsX() -1 )

        print 'Scale = %f, chi2 = %f' %( scale , this_chi2 )

        points.append( (scale, this_chi2) )

        #if scale > 1 and not drew_example:
        #if this_chi2 > 0.2 and not drew_example :
        if False :

            drew_example = True

            model.SetLineColor( ROOT.kBlue )
            model.SetMarkerColor( ROOT.kBlue )

            model.Draw()

            data.Draw('same')

            sig.SetLineColor( ROOT.kRed )
            sig.SetMarkerColor( ROOT.kRed )

            sig.Draw('same')

            #can = ROOT.TCanvas( str(uuid.uuid4()), '' )
            #frame = x_var.frame()
            #data_hist.plotOn(frame)
            #model.plotOn(frame)
            #frame.SetTitle('')

            #frame.Draw()

            raw_input("cont")

    return points


main()
