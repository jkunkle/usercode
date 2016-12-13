
import uuid

import ROOT
from SampleManager import SampleManager
from SampleManager import Sample



#ptbins = [(15,25), (25,35), (35,45)]
ptbins = [ (15,25), (25,35), (35,45)]
regions = ['EB', 'EE']


draw_base_real = ''


binnings = { 'EB' : {
                     'ph_sigmaIEIE' : ( 30, 0, 0.03), 'ph_chIsoCorr' : (40, 0, 52.4), 'ph_phoIsoCorr' : (30, 0, 39.9),
                    },
             'EE' : {
                      'ph_sigmaIEIE' : ( 30, 0, 0.0801), 'ph_chIsoCorr' : (40, 0, 50), 'ph_phoIsoCorr' : (50, 0, 51),
                    }
             }

loose_cuts = { 'EB' : {
                     'ph_sigmaIEIE' : 0.014,  'ph_chIsoCorr' : 5.24, 'ph_phoIsoCorr' : 5.32,
                    },
               'EE' : {
                      'ph_sigmaIEIE' : 0.1068, 'ph_chIsoCorr' : 5, 'ph_phoIsoCorr' : 4.08,
                      }
             }
cut_values = { 'EB' : {
                     'ph_sigmaIEIE' : 0.01,  'ph_chIsoCorr' : 1.31, 'ph_phoIsoCorr' : 1.33,
                    },
               'EE' : {
                      'ph_sigmaIEIE' : 0.0267, 'ph_chIsoCorr' : 1.25, 'ph_phoIsoCorr' : 1.02,
                      }
             }




def get_fake_draw_var( fitvar ) :

    if fitvar == 'ph_sigmaIEIE' :
        return 'probeph_sigmaIEIE'
    elif fitvar == 'ph_chIsoCorr' :
        return 'probeph_chHadIso'

def get_real_draw_var( fitvar ) :

    if fitvar == 'ph_sigmaIEIE' :
        return 'ph_sigmaIEIE[ptSorted_ph_mediumNoSIEIENoEleVeto_idx[0]]'
    elif fitvar == 'ph_chIsoCorr' :
        return 'ph_chIsoCorr[ptSorted_ph_mediumNoChIsoNoEleVeto_idx[0]]'

def get_fake_draw_str( data_mc, fitvar, reg, ptmin, ptmax ) :


    if fitvar == 'ph_sigmaIEIE' :
        photon_cuts = 'probeph_passChIsoCorrMedium && probeph_passNeuIsoCorrMedium && probeph_passPhoIsoCorrMedium'
    elif fitvar == 'ph_chIsoCorr'  :
        photon_cuts = 'probeph_passSIEIEMedium && probeph_passNeuIsoCorrMedium && probeph_passPhoIsoCorrMedium'

    if ptmax == None :
        pt_cuts = 'probeph_pt > %d' %ptmin
    else :
        pt_cuts = 'probeph_pt > %d && probeph_pt < %d ' %( ptmin, ptmax )

    reg_cuts = 'probeph_Is%s ' %reg

    if data_mc == 'data' :
        draw_str = '( 30.*( tagph_pt < 23 ) + 16.3*( tagph_pt > 23 && tagph_pt < 36) +3.22*( tagph_pt > 36 && tagph_pt < 49) + 2.8*(tagph_pt > 49 && tagph_pt < 77 ) + 2.0*( tagph_pt > 77 && tagph_pt < 90 ) + 1.6*( tagph_pt > 90 && tagph_pt < 122 ) + 1.3* ( tagph_pt > 122 && tagph_pt < 180 ) + 1.0*(tagph_pt > 180) ) * ( %s && %s && %s) '%( photon_cuts, reg_cuts, pt_cuts )
    else :
        draw_str = '%s && %s && %s ' %( photon_cuts, reg_cuts, pt_cuts )

    return draw_str

def get_real_draw_str( temp_sig, fitvar, reg, ptmin, ptmax, channel=None) :

    if fitvar == 'ph_sigmaIEIE' :
        phidx = 'ptSorted_ph_mediumNoSIEIENoEleVeto_idx'
        phcut = 'ph_mediumNoSIEIENoEleVeto_n==1'
    elif fitvar == 'ph_chIsoCorr' :
        phidx = 'ptSorted_ph_mediumNoChIsoNoEleVeto_idx'
        phcut = 'ph_mediumNoChIsoNoEleVeto_n==1'

    if temp_sig == 'template' :
        draw_base = 'mu_n==2 && m_mumu > 60 && ph_truthMatch_ph[%s[0]] && abs(ph_truthMatchMotherPID_ph[%s[0]]) < 25 ' %( phidx, phidx )
    elif temp_sig == 'signal' :
        if channel == 'Muon' :
            draw_base = 'mu_n==2 && (passTrig_Mu17_TkMu8_DZ || passTrig_Mu17_Mu8_DZ) && m_mumu > 60 && dr_leadLep_phot[%s[0]] > 0.7 && dr_sublLep_phot[%s[0]] > 0.7 ' %( phidx, phidx )
        elif channel == 'Electron' :
            draw_base = 'el_n==2 && m_elel > 60 && passTrig_Ele17_Ele12_DZ && dr_leadLep_phot[%s[0]] > 0.7 && dr_sublLep_phot[%s[0]] > 0.7 ' %( phidx, phidx )


    if ptmax == None :
        pt_cuts = 'ph_pt[%s[0]] > %d' %( phidx, ptmin )
    else :
        pt_cuts = 'ph_pt[%s[0]] > %d && ph_pt[%s[0]] < %d ' %( phidx, ptmin, phidx, ptmax )

    reg_cuts = 'ph_Is%s[%s[0]] ' %(reg, phidx)

    return '%s && %s && %s && %s' %( draw_base, phcut, reg_cuts, pt_cuts )


def main() :

    global sampManFake
    global sampManReal
    global sampManSignal

    base_dir_fake = '/data/users/jkunkle/RecoPhoton/FakePhotonProbeWithTrig_2015_11_27'
    base_dir_real = '/data/users/jkunkle/RecoPhoton/LepLepNoPhID_2015_11_26'
    base_dir_sig = '/data/users/jkunkle/RecoPhoton/LepLepNoPhID_2015_11_26'

    treeName = 'tupel/EventTree'
    xsfile = 'cross_sections/photon15.py'
    lumi = 2093.

    sampManFake   = SampleManager( base_dir_fake, treeName, filename='tree.root', xsFile=xsfile, lumi=lumi )
    sampManReal   = SampleManager( base_dir_real, treeName, filename='tree.root', xsFile=xsfile, lumi=lumi )
    sampManSignal = SampleManager( base_dir_sig, treeName, filename='tree.root', xsFile=xsfile, lumi=lumi )

    conf_fake = 'Modules/SinglePhoton15.py'
    conf_real = 'Modules/LepLep15.py'
    conf_signal = 'Modules/LepLep15.py'

    sampManFake.ReadSamples( conf_fake )
    sampManReal.ReadSamples( conf_real )
    sampManSignal.ReadSamples( conf_signal )

    channels = ['Muon',]
    #channels = ['Muon', 'Electron']


    fitvars = ['ph_chIsoCorr']
    #fitvars = ['ph_sigmaIEIE']

    # make fake photon templ

    for fv in fitvars :
        for reg in regions :

            for ptmin, ptmax in ptbins :

                fake_str_data = get_fake_draw_str( 'data', fv, reg, ptmin, ptmax )
                fake_str_mc = get_fake_draw_str( 'mc', fv, reg, ptmin, ptmax )
                draw_var_fake = get_fake_draw_var( fv )
                draw_var_real = get_real_draw_var( fv )

                real_str = get_real_draw_str( 'template', fv, reg, ptmin, ptmax )

                data_samp_fake = sampManFake.get_samples(name='SinglePhoton')[0]
                mc_samp_fake = sampManFake.get_samples(name='DiPhoton')[0]

                mc_samp_real = sampManReal.get_samples(name='Zgamma')[0]

                    
                data_template_fake = clone_sample_and_draw( data_samp_fake, draw_var_fake, fake_str_data, binnings[reg][fv],sampManFake )
                mc_template_fake = clone_sample_and_draw( mc_samp_fake, draw_var_fake, fake_str_mc, binnings[reg][fv],sampManFake )

                mc_template_real = clone_sample_and_draw( mc_samp_real, draw_var_real, real_str, binnings[reg][fv], sampManReal )

                data_template_fake.Add( mc_template_fake, -1 )

                #data_template_fake.Draw()
                #raw_input('cont')
                #mc_template_real.Draw()
                #raw_input('cont')


                for ch in channels :

                    signal_str = get_real_draw_str( 'signal', fv, reg, ptmin, ptmax, channel=ch )

                    data_samp_sig = sampManReal.get_samples(name=ch)[0]

                    sig_data = clone_sample_and_draw( data_samp_sig, draw_var_real, signal_str, binnings[reg][fv], sampManSignal )

                    xvar = ROOT.RooRealVar( 'xvar', 'xvar', 0, binnings[reg][fv][2] )

                    fakefrac = ROOT.RooRealVar( 'fakefrac', 'fakefrac', 0.5, 0., 1. )



                    sig_templatehist = ROOT.RooDataHist( 'sig_hist', 'sig_hist', ROOT.RooArgList(xvar), mc_template_real ) 
                    bkg_templatehist = ROOT.RooDataHist( 'bkg_hist', 'bkg_hist', ROOT.RooArgList(xvar), data_template_fake) 

                    sig_template = ROOT.RooHistPdf( 'sig_template', 'sig_template', ROOT.RooArgSet( xvar), sig_templatehist )
                    bkg_template = ROOT.RooHistPdf( 'bkg_template', 'bkg_template', ROOT.RooArgSet( xvar), bkg_templatehist)

                    model = ROOT.RooAddPdf( 'model', 'model', ROOT.RooArgList( sig_template, bkg_template), ROOT.RooArgList( fakefrac ) )

                    target_template = ROOT.RooDataHist( 'target_template', 'target_template', ROOT.RooArgList( xvar ), sig_data )

                    print 'RUN FIT'

                    result = model.fitTo( target_template, ROOT.RooFit.Range(0, loose_cuts[reg][fv]),ROOT.RooFit.Save()  )
                    if result is not None :
                        result.Print()
                        print 'Integral bins = 1 - %d' %(mc_template_real.FindBin(cut_values[reg][fv]))

                        print 'Predictd bkg = ', mc_template_real.Integral( 1, mc_template_real.FindBin(cut_values[reg][fv])-1 ) * fakefrac.getValV()

                    frame = xvar.frame()
                    target_template.plotOn(frame)
                    model.plotOn( frame )
                    model.plotOn( frame , ROOT.RooFit.Components('sig_template'), ROOT.RooFit.LineStyle(ROOT.kDashed))
                    model.plotOn( frame , ROOT.RooFit.Components('bkg_template'), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kRed ) )

                    frame.Draw()
                    raw_input('cont')

                    print result

                                         

def clone_sample_and_draw( samp, var, sel, binning, useSampMan ) :


    newSamp = useSampMan.clone_sample( oldname=samp.name, newname=samp.name+str(uuid.uuid4()), temporary=True ) 
    useSampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist


main()
