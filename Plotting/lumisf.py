
from uncertainties import ufloat

import math


def main() :

    ndata_el = ufloat( 37, math.sqrt(37 ) )

    ndata_el_leadsb =  ufloat( 11, math.sqrt( 11 )  )
    ndata_el_sublsb = ufloat( 9, math.sqrt( 9 ) )

    nbkg_el_statsr = ufloat( 14.209, 0.691  )
    nbkg_el_statsb = ufloat( 14.209, 0.594  )
    nbkg_el_crosscorr = ufloat( 0.0, 1.42  )
    nbkg_el_systbkg   = ufloat( 0.0, 2.84  )
    nbkg_el_systtemp  = ufloat( 0.0, 0.792 )
    nbkg_el_stat1d    = ufloat( 0.0, 0.48  )
    nbkg_el_statff    = ufloat( 0.0, 0.366 )

    nbkg_el_tot = ufloat( nbkg_el_statsr.n, 0.0 )
    nbkg_el_tot += nbkg_el_crosscorr 
    nbkg_el_tot += nbkg_el_systbkg   
    nbkg_el_tot += nbkg_el_systtemp  
    nbkg_el_tot += nbkg_el_stat1d    
    nbkg_el_tot += nbkg_el_statff    

    nbkg_elleadsb_statsr = ufloat( 6.036, 0.174 )
    nbkg_elleadsb_statsb = ufloat( 6.036, 0.219 )
    nbkg_elleadsb_crosscorr = ufloat( 0.0, 0.604  )
    nbkg_elleadsb_systbkg   = ufloat( 0.0, 1.12  )
    nbkg_elleadsb_systtemp  = ufloat( 0.0, 0.240 )
    nbkg_elleadsb_stat1d    = ufloat( 0.0, 0.189  )
    nbkg_elleadsb_statff    = ufloat( 0.0, 0.265 )

    nbkg_elleadsb_tot = ufloat( nbkg_elleadsb_statsr.n, 0.0 )
    nbkg_elleadsb_tot += nbkg_elleadsb_crosscorr 
    nbkg_elleadsb_tot += nbkg_elleadsb_systbkg   
    nbkg_elleadsb_tot += nbkg_elleadsb_systtemp  
    nbkg_elleadsb_tot += nbkg_elleadsb_stat1d    
    nbkg_elleadsb_tot += nbkg_elleadsb_statff    

    nbkg_elsublsb_statsr = ufloat( 8.286, 0.304 )
    nbkg_elsublsb_statsb = ufloat( 8.286, 0.371 )
    nbkg_elsublsb_crosscorr = ufloat( 0.0, 0.829  )
    nbkg_elsublsb_systbkg   = ufloat( 0.0, 1.96  )
    nbkg_elsublsb_systtemp  = ufloat( 0.0, 0.392 )
    nbkg_elsublsb_stat1d    = ufloat( 0.0, 0.330  )
    nbkg_elsublsb_statff    = ufloat( 0.0, 0.160 )

    nbkg_elsublsb_tot = ufloat( nbkg_elsublsb_statsr.n, 0.0 )
    nbkg_elsublsb_tot += nbkg_elsublsb_crosscorr 
    nbkg_elsublsb_tot += nbkg_elsublsb_systbkg   
    nbkg_elsublsb_tot += nbkg_elsublsb_systtemp  
    nbkg_elsublsb_tot += nbkg_elsublsb_stat1d    
    nbkg_elsublsb_tot += nbkg_elsublsb_statff    

    ndata_mu = ufloat( 108, math.sqrt( 108 ) )

    nbkg_mu_statSR =  ufloat(62.98, 1.31)
    nbkg_mu_statSB =  ufloat( 62.98, 1.36 )

    nbkg_mu_crosscorr = ufloat( 0.0, 6.3 )
    nbkg_mu_systbkg = ufloat( 0.0, 8.85 )
    nbkg_mu_systtemp = ufloat( 0.0, 1.78 )
    nbkg_mu_stat1d = ufloat( 0.0, 1.09 )
    nbkg_mu_statff = ufloat( 0.0, 1.15 )

    nbkg_mu_tot = ufloat( nbkg_mu_statSR.n, 0.0 )

    nbkg_mu_tot += nbkg_mu_crosscorr 
    nbkg_mu_tot += nbkg_mu_systbkg 
    nbkg_mu_tot += nbkg_mu_systtemp 
    nbkg_mu_tot += nbkg_mu_stat1d 
    nbkg_mu_tot += nbkg_mu_statff 

    print nbkg_mu_tot


    for i in range( 1, 100 ) :

        ndata_mod = ufloat( ndata_mu.n*i, math.sqrt( ndata_mu.n*i ) )

        nbkg_mod_statSB = ufloat( nbkg_mu_statSB.n*i, math.sqrt(i)* nbkg_mu_statSB.s )
        nbkg_mod_statSR = ufloat( nbkg_mu_statSR.n*i, math.sqrt(i)* nbkg_mu_statSR.s )

        nbkg_mu_mod = ufloat( i * nbkg_mu_tot.n, i* nbkg_mu_tot.s )
                        
        num = calc_xs_mu(ndata_mod, nbkg_mod_statSR, nbkg_mod_statSB, nbkg_mu_mod )

        print 'Scale = %d, numerator = %s, fractional error = %f' %( i, num, num.s/num.n )


    print
    print
    print 'Electron channel'
    for i in range( 1, 100 ) :

        ndata_mod = ufloat( ndata_el.n*i, math.sqrt( ndata_el.n*i ) )
        ndata_leadsb_mod = ufloat( ndata_el_leadsb.n*i, math.sqrt( ndata_el_leadsb.n*i ) )
        ndata_sublsb_mod = ufloat( ndata_el_sublsb.n*i, math.sqrt( ndata_el_sublsb.n*i ) )

        nbkg_el_statsr_mod = ufloat( nbkg_el_statsr.n*i, math.sqrt(i) * nbkg_el_statsr.s )
        nbkg_el_statsb_mod = ufloat( nbkg_el_statsb.n*i, math.sqrt(i) * nbkg_el_statsb.s )

        nbkg_elleadsb_statsr_mod = ufloat( nbkg_elleadsb_statsr.n*i, math.sqrt(i) * nbkg_elleadsb_statsr.s )
        nbkg_elleadsb_statsb_mod = ufloat( nbkg_elleadsb_statsb.n*i, math.sqrt(i) * nbkg_elleadsb_statsb.s )

        nbkg_elsublsb_statsr_mod = ufloat( nbkg_elsublsb_statsr.n*i, math.sqrt(i) * nbkg_elsublsb_statsr.s )
        nbkg_elsublsb_statsb_mod = ufloat( nbkg_elsublsb_statsb.n*i, math.sqrt(i) * nbkg_elsublsb_statsb.s )

        

        num = calc_xs_el( ndata_mod, 
                    ndata_leadsb_mod, 
                    ndata_sublsb_mod, 
                    nbkg_el_statsr_mod, 
                    nbkg_el_statsb_mod, 
                    nbkg_el_tot, 
                    nbkg_elleadsb_statsr_mod, 
                    nbkg_elleadsb_statsb_mod, 
                    nbkg_elleadsb_tot, 
                    nbkg_elsublsb_statsr_mod, 
                    nbkg_elsublsb_statsb_mod,
                    nbkg_elsublsb_tot)

        print 'Scale = %d, numerator = %s, fractional error = %f' %( i, num, num.s/num.n )
        

def calc_xs_el( ndata_sr, ndata_leadsb, ndata_sublsb, nbkg_sr_statsr, nbkg_sr_statsb, nbkg_sr_syst, nbkg_leadsb_statsr, nbkg_leadsb_statsb, nbkg_leadsb_syst,  nbkg_sublsb_statsr, nbkg_sublsb_statsb, nbkg_sublsb_syst ) :

    ff = 0.9

    elefake_lead_statsr = ufloat( ndata_leadsb.n - nbkg_leadsb_statsr.n,  ndata_leadsb.s - nbkg_leadsb_statsr.s )
    elefake_subl_statsr = ufloat( ndata_sublsb.n - nbkg_sublsb_statsr.n,  ndata_sublsb.s - nbkg_sublsb_statsr.s )

    elefake_lead_statsb = ufloat( ndata_leadsb.n , 0.0) -  nbkg_leadsb_statsb
    elefake_subl_statsb = ufloat( ndata_sublsb.n , 0.0) -  nbkg_sublsb_statsb

    elefake_lead_statsb = elefake_lead_statsb + ufloat( 0.0, elefake_lead_statsr.s )
    elefake_subl_statsb = elefake_subl_statsb + ufloat( 0.0, elefake_subl_statsr.s )

    elefake_lead_statsb = elefake_lead_statsb*ff
    elefake_subl_statsb = elefake_subl_statsb*ff

    elefake_tot_statsb = elefake_lead_statsb + elefake_subl_statsb

    bkg_tot_statsb = elefake_tot_statsb + nbkg_sr_statsb

    numerator_statsb = ufloat( ndata_sr.n, 0.0 ) - bkg_tot_statsb

    elefake_statsr = ff*( ndata_leadsb + ndata_sublsb - nbkg_leadsb_statsb - nbkg_sublsb_statsb )

    elefake_statsr = ufloat( elefake_lead_statsr.n, 0.0 )


    numerator_statsr = ufloat( ndata_sr.n - nbkg_sr_statsr.n, ndata_sr.s - nbkg_sr_statsr.s )
    numerator_statsr = numerator_statsr - elefake_statsr

    bkg_tot_syst = ufloat( nbkg_sr_syst.n - ff*nbkg_leadsb_syst.n - ff*nbkg_sublsb_syst.n, nbkg_sr_syst.s - ff*nbkg_leadsb_syst.s - ff*nbkg_sublsb_syst.s  ) 
    bkg_tot_syst += ff* ufloat( ndata_leadsb.n, 0.0 ) + ff*ufloat( ndata_sublsb.n, 0.0 )

    numerator_syst = ufloat( ndata_sr.n, 0.0 ) - bkg_tot_syst

    print numerator_statsb 
    print numerator_statsr
    print numerator_syst

    return ufloat( numerator_syst.n, 0.0 ) + ufloat( 0.0, numerator_statsb.s ) + ufloat( 0.0, numerator_statsr.s )  + ufloat( 0.0, numerator_syst.s )







def calc_xs_mu( ndata_mu, nbkg_mu_statSR, nbkg_mu_statSB, bkg_mu_tot ) :

    xsnum_statSR =  ufloat( ndata_mu.n - nbkg_mu_statSR.n , ndata_mu.s - nbkg_mu_statSR.s )
    xsnum_statSB =  ndata_mu - nbkg_mu_statSB

    xsnum_syst = ufloat( ndata_mu.n, 0.0) - bkg_mu_tot

    xscomb = ufloat( xsnum_statSR.n, 0.0 ) + ufloat( 0.0, xsnum_statSR.s ) + ufloat( 0.0, xsnum_statSB.s ) + ufloat( 0.0, xsnum_syst.s )

    return xscomb






main()

