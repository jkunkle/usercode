
import ROOT
from array import array
# -----------------------------------------------------
# Setup CMSSW first, CMSSW_5_3_22_patch1 works
# -----------------------------------------------------
#ROOT.gSystem.Load( '/afs/cern.ch/user/j/jkunkle/Programs/MG5_aMC_v2_4_3/ExRootAnalysis/libExRootAnalysis.so')
ROOT.gSystem.Load( '/afs/cern.ch/user/j/jkunkle/Programs/MG5_aMC_v2_4_3/ExRootAnalysis/ExRootClasses_cc.so')
from ROOT import TSortableObject
from ROOT import TRootLHEFEvent
from ROOT import TRootLHEFParticle

import math

from argparse import ArgumentParser

_m_w = 80.385

parser = ArgumentParser()

parser.add_argument( '--input', dest='input', default=None, help='Path to input file' )
parser.add_argument( '--output', dest='output', default=None, help='Path to output file' )
parser.add_argument( '--makeTree', dest='makeTree', default=False, action='store_true', help='make a tree' )

options = parser.parse_args()

def main() :

    ifile = ROOT.TFile.Open( options.input, 'READ' )

    tree = ifile.Get('LHEF')

    ph_n = ROOT.TH1F( 'ph_n', 'photon multiplicity', 10, 0, 10 )
    lep_n = ROOT.TH1F( 'lep_n', 'lepton multiplicity', 10, 0, 10 )
    nu_n = ROOT.TH1F( 'nu_n', 'neutrino multiplicity', 10, 0, 10 )
    qk_n = ROOT.TH1F( 'qk_n', 'quark multiplicity', 10, 0, 10 )
    ph_pt = ROOT.TH1F( 'ph_pt', 'photon pT', 100, 0, 1000 )
    lep_pt = ROOT.TH1F( 'lep_pt', 'lepton pT', 100, 0, 1000 )
    nu_pt = ROOT.TH1F( 'nu_pt', 'neutrino pT', 100, 0, 1000 )
    m_lep_nu = ROOT.TH1F( 'm_lep_nu', 'lepton plus neutrino mass', 100, 0, 200 )
    mt_lep_nu = ROOT.TH1F( 'mt_lep_nu', 'lepton plus neutrino mass', 100, 0, 200 )
    mt_lep_nu_ph = ROOT.TH1F( 'mt_lep_nu_ph', 'lepton plus neutrino mass', 1000, 0, 4000 )
    m_lep_nuNoZ = ROOT.TH1F( 'm_lep_nuNoZ', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 100, 0, 200 )
    m_lep_nuNoZ_success = ROOT.TH1F( 'm_lep_nuNoZ_success', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 100, 0, 200 )
    m_lep_nuNoZ_fail = ROOT.TH1F( 'm_lep_nuNoZ_fail', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 100, 0, 200 )
    m_lep_nuNoZ_ph = ROOT.TH1F( 'm_lep_nuNoZ_ph', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 100, 0, 200 )
    m_lep_nuNoZ_ph_success = ROOT.TH1F( 'm_lep_nuNoZ_ph_success', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 100, 0, 200 )
    m_lep_nuNoZ_ph_fail = ROOT.TH1F( 'm_lep_nuNoZ_ph_fail', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 100, 0, 200 )
    m_lep_nuReco_success = ROOT.TH1F( 'm_lep_nuReco_success', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 100, 0, 200 )
    m_lep_nuReco_fail = ROOT.TH1F( 'm_lep_nuReco_fail', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 100, 0, 200 )
    m_lep_nuReco = ROOT.TH1F( 'm_lep_nuReco', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 100, 0, 200 )
    m_lep_nuReco_ph_success = ROOT.TH1F( 'm_lep_nuReco_ph_success', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 1000, 0, 4000 )
    m_lep_nuReco_ph_fail = ROOT.TH1F( 'm_lep_nuReco_ph_fail', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 1000, 0, 4000 )
    m_lep_nuReco_ph = ROOT.TH1F( 'm_lep_nuReco_ph', 'lepton plus neutrino mass, with neutrino z momentum set to zero', 1000, 0, 4000 )
    nuRecoSolutionsDiff = ROOT.TH1F( 'nuRecoSolutionsDiff', 'difference in quadratic solutions', 100, -200, 200 )
    nuRecoSolutionsAvg= ROOT.TH1F( 'nuRecoSolutionsAvg', 'average in quadratic solutions', 100, -200, 200 )
    nuRecoSolutionsAvgLep= ROOT.TH1F( 'nuRecoSolutionsAvgLep', 'average in quadratic solutions', 100, -200, 200 )
    m_lep_nu_ph = ROOT.TH1F( 'm_lep_nu_ph', 'lepton plus neutrino plus photon mass', 1000, 0, 4000 )
    m_q_q    = ROOT.TH1F( 'm_q_q', 'di-quark mass', 100, 0, 200 )
    m_q_q_ph = ROOT.TH1F( 'm_q_q_ph', 'di-quark plus photon mass', 1000, 0, 4000 )
    dphi_lep_ph = ROOT.TH1F( 'dphi_lep_ph', 'delta phi between lepton and photon', 50, -3.2, 3.2)
    dphi_lepnu_ph = ROOT.TH1F( 'dphi_lepnu_ph', 'delta phi between lepton+neutrino and photon', 50, -3.2, 3.2 )
    
    br_ph_pt = array( 'f', [0] )
    br_lep_pt = array( 'f', [0] )
    br_nu_pt = array( 'f', [0] )
    br_m_lep_nu_ph = array( 'f', [0] )
    br_m_lep_nu = array( 'f', [0] )
    br_m_lep_nuNoZ = array( 'f', [0] )
    br_m_lep_nuNoZ_ph = array( 'f', [0] )
    br_m_lep_nuReco = array( 'f', [0] )
    br_m_lep_nuReco_ph = array( 'f', [0] )
    br_nuReco_success = array( 'i', [0] )
    br_dphi_lep_nu = array(  'f', [0] )
    br_dr_lep_nu = array(  'f', [0] )
    br_deta_lep_nu = array(  'f', [0] )
    if options.makeTree :
        outFile = ROOT.TFile.Open( options.output, 'RECREATE' )
        outtree = ROOT.TTree( 'events', 'events' )
        outtree.Branch( 'ph_pt', br_ph_pt, 'ph_pt/F' )
        outtree.Branch( 'lep_pt', br_lep_pt, 'lep_pt/F' )
        outtree.Branch( 'nu_pt', br_nu_pt, 'nu_pt/F' )
        outtree.Branch( 'm_lep_nu_ph', br_m_lep_nu_ph, 'm_lep_nu_ph/F' )
        outtree.Branch( 'm_lep_nu', br_m_lep_nu, 'm_lep_nu/F' )
        outtree.Branch( 'm_lep_nuNoZ', br_m_lep_nuNoZ, 'm_lep_nuNoZ/F' )
        outtree.Branch( 'm_lep_nuNoZ_ph', br_m_lep_nuNoZ_ph, 'm_lep_nuNoZ_ph/F' )
        outtree.Branch( 'm_lep_nuReco', br_m_lep_nuReco, 'm_lep_nuReco/F' )
        outtree.Branch( 'm_lep_nuReco_ph', br_m_lep_nuReco_ph, 'm_lep_nuReco_ph/F' )
        outtree.Branch( 'nuReco_success', br_nuReco_success, 'nuReco_success/I' )
        outtree.Branch( 'dphi_lep_nu', br_dphi_lep_nu, 'dphi_lep_nu/F' )
        outtree.Branch( 'dr_lep_nu', br_dr_lep_nu, 'dr_lep_nu/F' )
        outtree.Branch( 'deta_lep_nu', br_deta_lep_nu, 'deta_lep_nu/F' )


    check_ph = [22]
    check_lep = [11, -11, 13, -13, 15, -15]
    check_nu = [12, -12, 14, -14, 16, -16]
    check_qk = [1, -1, 2, -2, 3, -3, 4, -4, 5, -5]


    for evt in tree :
        npart = tree.Event[0].Nparticles

        nulvs = []
        leplvs = []
        gamlvs = [] 
        qklvs = []
        for parti in range(0, npart) :
            apid = tree.Particle[parti].PID
            if apid in check_ph :
                gamlv = ROOT.TLorentzVector()
                gamlv.SetPxPyPzE( tree.Particle[parti].Px, tree.Particle[parti].Py,tree.Particle[parti].Pz, tree.Particle[parti].E )
                gamlvs.append( gamlv)

            if apid in check_lep :
                leplv = ROOT.TLorentzVector()
                leplv.SetPxPyPzE( tree.Particle[parti].Px, tree.Particle[parti].Py,tree.Particle[parti].Pz, tree.Particle[parti].E )
                leplvs.append( leplv )

            if apid in check_nu :
                nulv = ROOT.TLorentzVector()
                nulv.SetPxPyPzE( tree.Particle[parti].Px, tree.Particle[parti].Py,tree.Particle[parti].Pz, tree.Particle[parti].E )
                nulvs.append( nulv )

            if apid in check_qk :
                if tree.Particle[parti].Mother1 > 0 :
                    qklv = ROOT.TLorentzVector()
                    qklv.SetPxPyPzE( tree.Particle[parti].Px, tree.Particle[parti].Py,tree.Particle[parti].Pz, tree.Particle[parti].E )
                    qklvs.append( qklv )

        ph_n .Fill( len( gamlvs ) )
        lep_n.Fill( len( leplvs ) )
        nu_n .Fill( len( nulvs ) )
        qk_n .Fill( len( qklvs ) )

        if len( gamlvs ) == 1 :

            ph_pt.Fill( gamlvs[0].Pt()) 

        if len( leplvs ) == 1 :
            lep_pt.Fill( leplvs[0].Pt()) 

        if len( nulvs ) == 1 :
            nu_pt.Fill( nulvs[0].Pt() )


        if len( gamlvs ) == 1 and len( leplvs ) == 1 and len( nulvs ) == 1 :

            met = ROOT.TLorentzVector()
            met.SetPtEtaPhiM( nulvs[0].Pt(), 0.0, nulvs[0].Phi(), 0.0 )
            met_orig = ROOT.TLorentzVector( met )

            var_m_lep_nu = (leplvs[0] + nulvs[0]).M()
            var_m_lep_nu_ph = (leplvs[0] + nulvs[0] + gamlvs[0]).M()
            var_m_lep_nuNoZ = ( leplvs[0] + met ).M()
            var_m_lep_nuNoZ_ph = ( leplvs[0] + met + gamlvs[0] ).M()

            m_lep_nu.Fill( var_m_lep_nu )
            m_lep_nu_ph.Fill( var_m_lep_nu_ph )


            dphi_lep_ph.Fill( (leplvs[0].DeltaPhi( gamlvs[0] ) )  )
            dphi_lepnu_ph.Fill( (( leplvs[0] + nulvs[0] ).DeltaPhi( gamlvs[0] ) )  )


            mt_lep_nu.Fill( calc_mt( leplvs[0] , met ) )
            mt_lep_nu_ph.Fill( calc_mt( leplvs[0]+met , gamlvs[0] ) ) 

            m_lep_nuNoZ.Fill( var_m_lep_nuNoZ )  
            m_lep_nuNoZ_ph.Fill( var_m_lep_nuNoZ_ph )  

            solution1 =-1
            solution2 =-1

            result = get_wgamma_nu_pz( leplvs[0], met)

            met = result[0]

            print 'Met P orig = %f, met Z new = %f, met P new = %f' %( met_orig.P() , met.Pz() , met.P()  )
            
            success = result[1][0]
            solution1 = result[1][1]
            solution2 = result[1][2]

            nuRecoSolutionsDiff.Fill( solution1 - solution2 )
            nuRecoSolutionsAvg.Fill( (solution1 + solution2)/2. )
            nuRecoSolutionsAvgLep.Fill( ( ( solution1 - leplvs[0].Pz() ) + ( solution2 - leplvs[0].Pt() ) )/2. )

            var_m_lep_nuReco = ( leplvs[0] + met ).M() 
            var_m_lep_nuReco_ph = (leplvs[0] + gamlvs[0] + met ).M()

            m_lep_nuReco.Fill( var_m_lep_nuReco )
            m_lep_nuReco_ph .Fill( var_m_lep_nuReco_ph )

            if success :
                m_lep_nuNoZ_success     .Fill( ( leplvs[0] + met_orig ).M() )  
                m_lep_nuNoZ_ph_success     .Fill( ( leplvs[0] + met_orig + gamlvs[0] ).M() )  
                m_lep_nuReco_success    .Fill( ( leplvs[0] + met ).M() )
                m_lep_nuReco_ph_success .Fill( (leplvs[0] + gamlvs[0] + met ).M() )

            else :
                m_lep_nuNoZ_fail     .Fill( ( leplvs[0] + met_orig ).M() )  
                m_lep_nuNoZ_ph_fail     .Fill( ( leplvs[0] + met_orig + gamlvs[0] ).M() )  
                m_lep_nuReco_fail    .Fill( ( leplvs[0] + met ).M() )
                m_lep_nuReco_ph_fail .Fill( (leplvs[0] + gamlvs[0] + met ).M() )

            br_ph_pt[0] = gamlvs[0].Pt()
            br_lep_pt[0] = leplvs[0].Pt()
            br_nu_pt[0] = nulvs[0].Pt()
            br_m_lep_nu[0] = var_m_lep_nu
            br_m_lep_nu_ph[0] = var_m_lep_nu_ph
            br_m_lep_nuNoZ[0] = var_m_lep_nuNoZ
            br_m_lep_nuNoZ_ph[0] = var_m_lep_nuNoZ_ph
            br_m_lep_nuReco[0] = var_m_lep_nuReco
            br_m_lep_nuReco_ph[0] = var_m_lep_nuReco_ph
            br_nuReco_success[0] = success
            br_dphi_lep_nu[0] = leplvs[0].DeltaPhi( nulvs[0] )
            br_dr_lep_nu[0] = leplvs[0].DeltaR( nulvs[0] )
            br_deta_lep_nu[0] = math.fabs( leplvs[0].Eta() -  nulvs[0].Eta() )

            if options.makeTree :
                outtree.Fill()

        if len( gamlvs ) == 1 and len( qklvs ) == 2 :

            m_q_q.Fill( ( qklvs[0] + qklvs[1] ).M() )
            m_q_q_ph.Fill( ( qklvs[0] + qklvs[1] + gamlvs[0] ).M() )




    print 'Write file %s' %options.output
    outFile.cd()

    ph_n.Write()
    lep_n.Write()
    nu_n.Write()
    qk_n.Write()
    ph_pt.Write()
    lep_pt.Write()
    nu_pt.Write()
    m_lep_nu.Write()
    mt_lep_nu.Write()
    mt_lep_nu_ph.Write()
    m_lep_nuNoZ.Write()
    m_lep_nuNoZ_success.Write()
    m_lep_nuNoZ_fail.Write()
    m_lep_nuNoZ_ph.Write()
    m_lep_nuNoZ_ph_success.Write()
    m_lep_nuNoZ_ph_fail.Write()
    m_lep_nuReco_success.Write()
    m_lep_nuReco_fail.Write()
    m_lep_nuReco.Write()
    m_lep_nuReco_ph_success.Write()
    m_lep_nuReco_ph_fail.Write()
    m_lep_nuReco_ph.Write()
    nuRecoSolutionsDiff.Write()
    nuRecoSolutionsAvg.Write()
    nuRecoSolutionsAvgLep.Write()
    m_lep_nu_ph.Write()
    m_q_q.Write()
    m_q_q_ph.Write()
    dphi_lep_ph.Write()
    dphi_lepnu_ph.Write()


    if options.makeTree :
        outtree.Write()
    outFile.Close()



def get_wgamma_nu_pz( lepton, metlv ) :


    new_met = ROOT.TLorentzVector()

    calc_res = calc_constrained_nu_momentum( lepton, metlv )
    desc_pos = calc_res[0]
    solved_pz = calc_res[1]
    solution1 = calc_res[2]
    solution2 = calc_res[3]
    if desc_pos :
        new_met.SetXYZM( metlv.Px(), metlv.Py(),solved_pz, 0.0 )

    else :
        print "DISCRIMINANT IS NEGATIVE"

        alpha = ( lepton.Px()*metlv.Px() + lepton.Py()*metlv.Py() )/ metlv.Pt()
        delta = ( _m_w*_m_w - lepton.M()*lepton.M() )

        Aval = 4*lepton.Pz()*lepton.Pz() - 4*lepton.E()*lepton.E() +4*alpha*alpha
        Bval = 4*alpha*delta
        Cval = delta*delta

        success2 = solve_quadratic( Aval, Bval, Cval)

        if not success2[0] :
            print "SECOND FAILURE"

        scale1 = solution1/metlv.Pt()
        scale2 = solution2/metlv.Pt()

        metlv_sol1 = ROOT.TLorentzVector()
        metlv_sol2 = ROOT.TLorentzVector ()
        metlv_sol1.SetPtEtaPhiM( metlv.Pt()*scale1, 0.0, metlv.Phi(), 0.0 )
        metlv_sol2.SetPtEtaPhiM( metlv.Pt()*scale2, 0.0, metlv.Phi(), 0.0 )

        sol1 = calc_constrained_nu_momentum( lepton, metlv_sol1)
        sol2 = calc_constrained_nu_momentum( lepton, metlv_sol2)
        success_sol1 = sol1[0]
        success_sol2 = sol2[0]
        pz_sol1 = sol1[1]
        pz_sol2 = sol2[1]

        if not success_sol1  :
            print "FAILURE SOLUTION 1"
            metlv.SetPtEtaPhiM(-1, 0, 0, 0)
            return (False, -1, -1 )

        if not success_sol2 :
            print "FAILURE SOLUTION 2" 
            metlv.SetPtEtaPhiM(-1, 0, 0, 0)
            return (False, -1, -1 )

        solved_met3v_sol1 = ROOT.TVector3()
        solved_met3v_sol2 = ROOT.TVector3()
        solved_met3v_sol1.SetXYZ(metlv_sol1.Px(), metlv_sol1.Py(), pz_sol1)
        solved_met3v_sol2.SetXYZ(metlv_sol2.Px(), metlv_sol2.Py(), pz_sol2)
        solved_metlv_sol1 = ROOT.TLorentzVector ()
        solved_metlv_sol2 = ROOT.TLorentzVector ()
        solved_metlv_sol1.SetVectM( solved_met3v_sol1 , 0.0 )
        solved_metlv_sol2.SetVectM( solved_met3v_sol2 , 0.0 )

        wmass_sol1 = ( lepton + solved_metlv_sol1 ).M()
        wmass_sol2 = ( lepton + solved_metlv_sol2 ).M()

        if math.fabs( wmass_sol1 - _m_w ) < math.fabs( wmass_sol2 - _m_w ) :
            new_met= metlv_sol1
        else  :
            new_met = metlv_sol2
        
    return ( new_met, calc_res );

def calc_constrained_nu_momentum( lepton, met ) :

    little_a = _m_w*_m_w - lepton.M()*lepton.M() + 2*( lepton.Px()*met.Px() + lepton.Py()*met.Py() )

    Aval = ( 4*lepton.E()*lepton.E() ) - ( 4*lepton.Pz()*lepton.Pz() )
    Bval = -4 * little_a * lepton.Pz()

    Cval = 4*lepton.E()*lepton.E()*met.Pt()*met.Pt() - little_a*little_a

    quad_result= solve_quadratic( Aval, Bval, Cval)
    success = quad_result[0]
    solution1 = quad_result[1]
    solution2 = quad_result[2]

    result = -1
    if  success :
       if math.fabs(solution1- lepton.Pz() ) < math.fabs( solution2 - lepton.Pz() )  :
           result = solution1
       else :
           result = solution2
    return (success, result, solution1, solution2 )

def solve_quadratic( Aval, Bval, Cval) :

    discriminant = Bval*Bval - 4*Aval*Cval

    #print "DISCRIMINANT = ", discriminant

    if discriminant >= 0 :
       solution1 = ( -1*Bval + math.sqrt( discriminant ) ) / ( 2 * Aval ) 
       solution2 = ( -1*Bval - math.sqrt( discriminant ) ) / ( 2 * Aval )  
       return (True, solution1, solution2);
    else :
        return (False, -1, -1 );

def calc_mt( obj, nu ) :

     return math.sqrt( 2*obj.Pt()*nu.Pt() * ( 1 - math.cos( obj.DeltaPhi(nu) ) ) )


main()
