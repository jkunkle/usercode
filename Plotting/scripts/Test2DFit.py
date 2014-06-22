
import ROOT


def main() :

    x = ROOT.RooRealVar('x','x',0,100) 
    y = ROOT.RooRealVar('y','y',0,100)

    mean_sig_x  = ROOT.RooRealVar('mean_sig_x','Mean of Gaussian',20,0,100) 
    sigma_sig_x = ROOT.RooRealVar('sigma_sig_x','Width of Gaussian',3,0,100) 
    gauss_sig_x = ROOT.RooGaussian('gauss_sig_x','gauss(x,mean,sigma)',x,mean_sig_x,sigma_sig_x) 
    mean_sig_y  = ROOT.RooRealVar('mean_sig_y','Mean of Gaussian',20,0,100) 
    sigma_sig_y = ROOT.RooRealVar('sigma_sig_y','Width of Gaussian',3,0,100) 
    gauss_sig_y = ROOT.RooGaussian('gauss_sig_y','gauss(x,mean,sigma)',y,mean_sig_y,sigma_sig_y) 

    mean_bkg_x  = ROOT.RooRealVar('mean_bkg_x','Mean of Gaussian',30,0,100) 
    sigma_bkg_x = ROOT.RooRealVar('sigma_bkg_x','Width of Gaussian',10,0,100) 
    gauss_bkg_x = ROOT.RooGaussian('gauss_bkg_x','gauss(x,mean,sigma)',x,mean_bkg_x,sigma_bkg_x)
    mean_bkg_y  = ROOT.RooRealVar('mean_bkg_y','Mean of Gaussian',30,0,100) 
    sigma_bkg_y = ROOT.RooRealVar('sigma_bkg_y','Width of Gaussian',10,0,100) 
    gauss_bkg_y = ROOT.RooGaussian('gauss_bkg_y','gauss(x,mean,sigma)',y,mean_bkg_y,sigma_bkg_y)

    #testframe = x.frame()
    #gauss_sig_x.plotOn(testframe)
    #gauss_bkg_x.plotOn(testframe, ROOT.RooFit.LineStyle( ROOT.kDashed))
    #testframe.Draw()
    #raw_input('continue')

    sigfrac = ROOT.RooRealVar( 'sigfrac', 'sigfrac', 0.5, 0., 1.)

    sigmodel = ROOT.RooProdPdf( 'prod_sig', 'gauss_sig_x*gauss_sig_y', ROOT.RooArgList( gauss_sig_x, gauss_sig_y) )
    bkgmodel = ROOT.RooProdPdf( 'prod_bkg', 'gauss_bkg_x*gauss_bkg_y', ROOT.RooArgList( gauss_bkg_x, gauss_bkg_y) )

    model = ROOT.RooAddPdf('model','sig+bkg',ROOT.RooArgList(sigmodel, bkgmodel),ROOT.RooArgList(sigfrac)); 

    data = model.generate(ROOT.RooArgSet(x,y),1000000)
    datahist = ROOT.RooDataHist( 'datahist', 'datahist', ROOT.RooArgSet( x, y), data )

    histdata = datahist.createHistogram('hdata2d',x,ROOT.RooFit.Binning(100),ROOT.RooFit.YVar(y,ROOT.RooFit.Binning(100))) ; 
    histdata.Draw('colz')
    print histdata.Integral()
    raw_input('continue')
    hist2d = model.createHistogram('hmodel2d',x,ROOT.RooFit.Binning(100),ROOT.RooFit.YVar(y,ROOT.RooFit.Binning(100))) ; 

    hist2d.Draw('colz')
    raw_input('continue')
    
    bkg_min = [30, 35, 40, 45]

    bkgtesthist = gauss_bkg_x.createHistogram( 'bkgtesthist', x, ROOT.RooFit.Binning(100 ))

    for bm in bkg_min :

        bkg_prob = bkgtesthist.Integral(bm, 100)
        bkg_events = histdata.Integral( bm, 100, bm, 100 )

        print 'background_min = %d, background_prob = %f, predict %f total events' %( bm, bkg_prob, bkg_events/( bkg_prob*bkg_prob ) )

    #model.fitTo( datahist)
    frame = x.frame()
    model.plotOn(frame) 
    model.plotOn(frame, ROOT.RooFit.Components('gaus_sig_x'), ROOT.RooFit.LineStyle(ROOT.kDashed) )
    data.plotOn(frame)
    frame.Draw()
    raw_input('continue')

    framey = y.frame()
    model.plotOn(framey )
    data.plotOn(framey)
    framey.Draw()
    raw_input('continue')



main()

