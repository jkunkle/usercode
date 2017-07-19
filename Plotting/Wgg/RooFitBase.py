import ROOT
import uuid
import os
ROOT.gROOT.ProcessLine( '.L /afs/cern.ch/user/j/jkunkle/usercode/Plotting/etogammaFR_eg/RooCMSShape.cc+' )

def fit_model_to_data( var, data_hist, fit_defs, sampMan, signal=[], background=[], bkg_labels=[]) :

    if not hasattr( sampMan, 'fit_objs' ) :
        sampMan.fit_objs = {}

    if len(background) != len(bkg_labels) :
        print 'Please provide one label per background!'
        return 0

    for idx, sig in enumerate(signal) :

        if isinstance( sig, ROOT.RooDataSet ) :

            sampMan.fit_objs['mean'] = ROOT.RooRealVar('mean', 'Gaussian Z mass', fit_defs['mean'], -5, 5,'GeV/c^{2}')
            sampMan.fit_objs['sigma'] = ROOT.RooRealVar('sigma', '#sigma', fit_defs['sigma'], 0.2,4.0,'GeV/c^{2}')

            sampMan.fit_objs['gauss'] = ROOT.RooGaussian('gaussian','Signal shape gaussian',var, sampMan.fit_objs['mean'], sampMan.fit_objs['sigma'])

            sampMan.fit_objs['sig_template'] = ROOT.RooNDKeysPdf( 'sig_template', 'sig_template', ROOT.RooArgList(var), sig, "a", fit_defs['rho'], fit_defs['nSigma'] )
            #sampMan.fit_objs['sig_model'] = ROOT.RooNDKeysPdf( 'sig_model', 'sig_template', ROOT.RooArgList(var), MCSig, "a", fit_defs['rho'], fit_defs['nSigma'] )

            #  Convolution p.d.f. using numeric convolution operator based on Fourier Transforms
            sampMan.fit_objs['sig_model'] = ROOT.RooFFTConvPdf('sig_model','Convolution', var, sampMan.fit_objs['sig_template'], sampMan.fit_objs['gauss'])

        elif isinstance( sig, ROOT.TH1 ) :

            sampMan.fit_objs['mean'] = ROOT.RooRealVar('mean', 'Gaussian Z mass', fit_defs['mean'], -5, 5,'GeV/c^{2}')
            sampMan.fit_objs['sigma'] = ROOT.RooRealVar('sigma', '#sigma', fit_defs['sigma'], 0.2,4.0,'GeV/c^{2}')

            sampMan.fit_objs['gauss'] = ROOT.RooGaussian('gaussian','Signal shape gaussian',var, sampMan.fit_objs['mean'], sampMan.fit_objs['sigma'])

            sampMan.fit_objs['sig_template_hist'] = ROOT.RooDataHist( 'template_hist', 'template_hist', ROOT.RooArgList( var ), sig)
            sampMan.fit_objs['sig_template'] = ROOT.RooHistPdf( 'sig_template', 'sig_template', ROOT.RooArgSet( var ), sampMan.fit_objs['sig_template_hist'] )

            #  Convolution p.d.f. using numeric convolution operator based on Fourier Transforms
            sampMan.fit_objs['sig_model'] = ROOT.RooFFTConvPdf('sig_model','Convolution', var, sampMan.fit_objs['sig_template'], sampMan.fit_objs['gauss'])

        else :
            if sig == 'landau' :

                sampMan.fit_objs['mean'] = ROOT.RooRealVar( 'mean', 'Landau Mean', fit_defs['mean'], 0, 200, '' )
                sampMan.fit_objs['sigma'] = ROOT.RooRealVar( 'sigma', 'Landau Sigma', fit_defs['sigma'], 0, 100 , '' )

                sampMan.fit_objs['sig_model'] = ROOT.RooLandau( 'sig_model', 'Landau', var, sampMan.fit_objs['mean'], sampMan.fit_objs['sigma'])

            elif sig == 'bwxcb' :

                #  Parameters for Crystal Ball Lineshape
                sampMan.fit_objs['m0']    = ROOT.RooRealVar('#Delta m_{0}', 'Bias' , fit_defs['Bias'] , -3.0 , 2.0,'GeV/c^{2}')
                sampMan.fit_objs['sigma'] = ROOT.RooRealVar('#sigma_{CB}' , 'Width', fit_defs['Width'], 0.5  , 4.5, 'GeV/c^{2}')
                sampMan.fit_objs['cut']   = ROOT.RooRealVar('#alpha'      , 'Cut'  , fit_defs['Cut']  , -10.0, 0. , ''  )
                sampMan.fit_objs['power'] = ROOT.RooRealVar('#gamma'      , 'Power', fit_defs['Power'], 5    , 30 , ''  )

                #  Parameters for Breit-Wigner Distribution
                sampMan.fit_objs['mRes'] = ROOT.RooRealVar('M_{Z^{0}}', 'Z0 Resonance  Mass', 91.188, 88.0, 94.0,'GeV/c^{2}')
                sampMan.fit_objs['Gamma'] = ROOT.RooRealVar('#Gamma', '#Gamma', 2.495, 1,4.0,'GeV/c^{2}')
                sampMan.fit_objs['mRes'].setConstant()
                sampMan.fit_objs['Gamma'].setConstant()

                sampMan.fit_objs['cb'] = ROOT.RooCBShape('cb', 'A  Crystal Ball Lineshape', var, sampMan.fit_objs['m0'], sampMan.fit_objs['sigma'], sampMan.fit_objs['cut'], sampMan.fit_objs['power'])
                #  Breit-Wigner Lineshape
                sampMan.fit_objs['bw'] = ROOT.RooBreitWigner('bw','A Breit-Wigner Distribution', var, sampMan.fit_objs['mRes'],sampMan.fit_objs['Gamma'])

                #  Convolution p.d.f. using numeric convolution operator based on Fourier Transforms
                sampMan.fit_objs['sig_model'] = ROOT.RooFFTConvPdf('sig_model','Convolution', var, sampMan.fit_objs['bw'], sampMan.fit_objs['cb'])

    for bkg, lab in zip(background, bkg_labels) :

        if isinstance( bkg, ROOT.RooDataSet ) :
            sampMan.fit_objs[lab] = ROOT.RooNDKeysPdf( lab, 'bkg_template', ROOT.RooArgList(var), bkg, "a", fit_defs['rho'], fit_defs['nSigma'] )

        elif isinstance( bkg, ROOT.TH1 ) :

            sampMan.fit_objs['bkg_template_hist'] = ROOT.RooDataHist( 'template_hist', 'template_hist', ROOT.RooArgList( var ), bkg )
            sampMan.fit_objs[lab] = ROOT.RooHistPdf( lab, 'bkg_template', ROOT.RooArgSet( var ), sampMan.fit_objs['bkg_template_hist'] )

            #sampMan.fit_objs['bkg_model %idx'] = ROOT.RooFFTConvPdf('bkg_model','Convolution', var, sampMan.fit_objs['bkg_template'], sampMan.fit_objs['gauss'])

        else :
            if bkg == 'poly' :
                sampMan.fit_objs['poly_1'] = ROOT.RooRealVar( 'poly_1', 'linear term'   , fit_defs['poly_linear']   , -1000, 1000, '' )
                sampMan.fit_objs['poly_2'] = ROOT.RooRealVar( 'poly_2', 'quadratic term', fit_defs['poly_quadratic'], -1000, 0   , '' )
                sampMan.fit_objs['poly_3'] = ROOT.RooRealVar( 'poly_3', 'cubic term'    , fit_defs['poly_cubic']    , -100 , 100 , '' )
                sampMan.fit_objs['poly_4'] = ROOT.RooRealVar( 'poly_4', 'quartic term'  , fit_defs['poly_quartic']  , -100 , 100 , '' )

                sampMan.fit_objs[lab] = ROOT.RooPolynomial(lab, 'Cubic polynomial', var, ROOT.RooArgList(sampMan.fit_objs['poly_1'], sampMan.fit_objs['poly_2'], sampMan.fit_objs['poly_3'], sampMan.fit_objs['poly_4']))
            elif bkg == 'exp' :
                sampMan.fit_objs['width'] = ROOT.RooRealVar ('width', 'exponential width', fit_defs['exp_width'], -10, 10 )
                sampMan.fit_objs[lab] = ROOT.RooExponential( lab, 'Exponential', var,  sampMan.fit_objs['width'] )
            elif bkg == 'cheby' :

                sampMan.fit_objs['cheby_a0'] = ROOT.RooRealVar ('a0', 'chebychev 0', fit_defs['a0'], -10, 10 )
                sampMan.fit_objs['cheby_a1'] = ROOT.RooRealVar ('a1', 'chebychev 1', fit_defs['a1'], -10, 10 )
                sampMan.fit_objs['cheby_a2'] = ROOT.RooRealVar ('a2', 'chebychev 2', fit_defs['a2'], -10, 10 )

                sampMan.fit_objs[lab] = ROOT.RooChebychev( lab, 'Chebychev',  var, ROOT.RooArgList( sampMan.fit_objs['cheby_a0'], sampMan.fit_objs['cheby_a1'], sampMan.fit_objs['cheby_a2']) )
            elif bkg == 'bernstein' :

                sampMan.fit_objs['bern_b0'] = ROOT.RooRealVar ('b0', 'bernstein 0', fit_defs['b0'], -10, 10 )
                sampMan.fit_objs['bern_b1'] = ROOT.RooRealVar ('b1', 'bernstien 1', fit_defs['b1'], -10, 10 )
                sampMan.fit_objs['bern_b2'] = ROOT.RooRealVar ('b2', 'bernstien 2', fit_defs['b2'], -10, 10 )

                sampMan.fit_objs[lab] = ROOT.RooBernstein( lab, 'Bernstein',  var, ROOT.RooArgList( sampMan.fit_objs['bern_b0'], sampMan.fit_objs['bern_b1'], sampMan.fit_objs['bern_b2']) )

            elif bkg == 'cmsshape' :

                # Generate ROOCMSShape
                sampMan.fit_objs['cms_alpha'] = ROOT.RooRealVar('cms_alpha', 'cms_alpha', fit_defs['cms_alpha'], 20, 200, '')
                sampMan.fit_objs['cms_beta']  = ROOT.RooRealVar('cms_beta' , 'cms_beta' , fit_defs['cms_beta'] , 0., 0.8  , '')
                sampMan.fit_objs['cms_gamma'] = ROOT.RooRealVar('cms_gamma', 'cms_gamma', fit_defs['cms_gamma'], 0 , 0.3, '')
                sampMan.fit_objs['cms_peak']  = ROOT.RooRealVar('cms_peak' , 'cms_peak' , fit_defs['cms_peak'] , 85, 95 , '')

                sampMan.fit_objs[lab] = ROOT.RooCMSShape(lab, 'CMSShape', var, sampMan.fit_objs['cms_alpha'], sampMan.fit_objs['cms_beta'], sampMan.fit_objs['cms_gamma'], sampMan.fit_objs['cms_peak'])


    sig_bkg_models = ROOT.TObjArray()
    sig_bkg_models.Add( sampMan.fit_objs['sig_model'] )
    bkg_models = []
    for lab in bkg_labels :
        bkg_models.append( sampMan.fit_objs[lab] )
        sig_bkg_models.append( sampMan.fit_objs[lab] )

    # fitted values
    sampMan.fit_objs['nsig'] = ROOT.RooRealVar('N_{S}', '#signal events'    , fit_defs['nsig'],0,1000000.)

    sig_bkg_vars = ROOT.TObjArray()
    sig_bkg_vars.Add( sampMan.fit_objs['nsig'] )

    bkg_vars = ROOT.TObjArray()
    for bkg_model, bkg_label in zip( bkg_models, bkg_labels ) :
        var_lab = 'N ' + bkg_label
        sampMan.fit_objs[var_lab] = ROOT.RooRealVar(var_lab, 'background events', 100,0,1000000.)
        sig_bkg_vars.Add( sampMan.fit_objs[var_lab] )

    sampMan.fit_objs['model'] = ROOT.RooAddPdf('model', 'Di-photon Mass model', ROOT.RooArgList(sig_bkg_models), ROOT.RooArgList(sig_bkg_vars))

    # data
    sampMan.fit_objs['target_data'] = ROOT.RooDataHist( 'target_data', 'target_data', ROOT.RooArgList(var), data_hist)

    sampMan.fit_objs['fit_result'] = sampMan.fit_objs['model'].fitTo(sampMan.fit_objs['target_data'],ROOT.RooFit.Range(fit_defs['fit_min'], fit_defs['fit_max']),ROOT.RooFit.SumW2Error(True),ROOT.RooFit.Save())

    chi2 = sampMan.fit_objs['model'].createChi2(sampMan.fit_objs['target_data'],ROOT.RooFit.Range(fit_defs['fit_min'], fit_defs['fit_max']))

    return chi2

def draw_fitted_results( model, target_data, sig_model, bkg_models, var, chi2, label, outputName=None ) :

    if not isinstance( bkg_models, list ) :
        bkg_models = [bkg_models]

    can = ROOT.TCanvas( str(uuid.uuid4()), '' )
    frame = var.frame()
    target_data.plotOn(frame)
    model.plotOn(frame)
    model.plotOn(frame, ROOT.RooFit.Components('sig_model'), ROOT.RooFit.LineStyle(ROOT.kDashed)) 
    for bkg in bkg_models :
        model.plotOn(frame, ROOT.RooFit.Components(bkg), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kRed ) ) 
    frame.SetTitle('')
    model.Print()

    frame.Draw()
    lab = ROOT.TLatex( 0.6, 0.85, label  )
    lab.SetNDC()
    lab.SetX(0.4)
    lab.SetY(0.91)
    lab.Draw()

    chi2lab = ROOT.TLatex( 0.1, 0.91, '#chi^{2}/NDF = %.2f' %(chi2.getVal()/(target_data.createHistogram( str(uuid.uuid4()), var, ).GetNbinsX() -1 )) )
    chi2lab.SetNDC()
    chi2lab.SetX(0.1)
    chi2lab.SetY(0.91)
    chi2lab.Draw()

    if outputName is None :
        model.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
        frame.Draw()
        lab.Draw()
        chi2lab.Draw()
        raw_input('continue')
    else :
        name = outputName + '.pdf'
        name_log = outputName + '__logy.pdf'
        name_nopar = outputName + '__nopar.pdf'
        if not os.path.isdir( os.path.split( name )[0] ) :
            os.makedirs( os.path.split( name )[0] )
        can.SetLogy()
        can.SaveAs(name_nopar)
        model.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
        frame.Draw()
        lab.Draw()
        chi2lab.Draw()
        can.SetLogy(0)
        can.SaveAs(name)
        can.SetLogy()
        can.SaveAs(name_log)

def SetHistContentBins( hist, eff, etamin, etamax, ptmin, ptmax ) :

    if eff is None :
        return

    for xbin in range( 1, hist.GetNbinsX()+1) :
        for ybin in range( 1, hist.GetNbinsY()+1) :
            xmin = hist.GetXaxis().GetBinLowEdge(xbin)
            xmax = hist.GetXaxis().GetBinUpEdge(xbin)
            ymin = hist.GetYaxis().GetBinLowEdge(ybin)
            ymax = hist.GetYaxis().GetBinUpEdge(ybin)

            if (xmin+0.001) >= etamin and (xmax-0.001) <= etamax and (ymin+0.001) >= ptmin and (ymax-0.001) <= ptmax :
                hist.SetBinContent( xbin, ybin, eff.n )
                hist.SetBinError( xbin, ybin, eff.s )

