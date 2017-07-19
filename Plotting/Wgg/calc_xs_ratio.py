import ROOT
import math

def main()  :

    filename_isr = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/WAANLOTruth_2015_06_26/job_NLO_WAA_ISR/Job_0000/tree.root'
    filename_fsr = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/WAANLOTruth_2015_06_26/job_NLO_WAA_FSR/Job_0000/tree.root'
    #filename_isr = 'root://eoscms//eos/cms/store/user/jkunkle/Wgamgam/SignalTruth_2014_03_06/job_summer12_WAA_ISR/Job_0000/tree.root'
    #filename_fsr = 'root://eoscms//eos/cms/store/user/jkunkle/Wgamgam/SignalTruth_2014_03_06/job_summer12_Wgg_FSR/Job_0000/tree.root'

    file_isr = ROOT.TFile.Open( filename_isr, 'READ' )
    file_fsr = ROOT.TFile.Open( filename_fsr, 'READ' )

    tree_isr = file_isr.Get('ggNtuplizer/EventTree' )
    tree_fsr = file_fsr.Get('ggNtuplizer/EventTree' )

    #print 'ISR, 15 GeV ', get_events( tree_isr, lepton_pt_cut =0, lepton_eta_cut=0, photon_pt_cut=0, photon_eta_cut=0, lead_photon_pt_cut=0 )
    print 'ISR, 15 GeV ', get_events( tree_isr, lepton_pt_cut =25, lepton_eta_cut=2.5, photon_pt_cut=15, photon_eta_cut=2.5, lead_photon_pt_cut=15 )
    print 'FSR, 15 GeV ', get_events( tree_fsr, lepton_pt_cut =25, lepton_eta_cut=2.5, photon_pt_cut=15, photon_eta_cut=2.5, lead_photon_pt_cut=15 )
    print 'ISR, 40 GeV ', get_events( tree_isr, lepton_pt_cut =25, lepton_eta_cut=2.5, photon_pt_cut=15, photon_eta_cut=2.5, lead_photon_pt_cut=40 )
    print 'FSR, 40 GeV ', get_events( tree_fsr, lepton_pt_cut =25, lepton_eta_cut=2.5, photon_pt_cut=15, photon_eta_cut=2.5, lead_photon_pt_cut=40 )

def get_events( tree, lepton_pt_cut=0, lepton_eta_cut=3.0, photon_pt_cut=0, photon_eta_cut=3.0, lead_photon_pt_cut=0 ) :

    n_total = 0
    n_pass = 0
    for event in range(0,tree.GetEntries()) :
        n_total += 1
        leptons = []
        leptons_noid = []
        photons = []
        neutrinos = []
        tree.GetEntry(event)

        for idx in range( 0, tree.nMC ) :

            if abs(tree.mcPID[idx]) == 11 or abs(tree.mcPID[idx]) == 13 :
                if tree.mcPt[idx] > lepton_pt_cut and math.fabs( tree.mcEta[idx] ) < lepton_eta_cut :
                    if abs(tree.mcMomPID[idx]) == 24 or abs(tree.mcMomPID[idx]) == 15 :
                        tlv = ROOT.TLorentzVector()
                        tlv.SetPtEtaPhiE( tree.mcPt[idx], tree.mcEta[idx], tree.mcPhi[idx], tree.mcE[idx] )
                        leptons.append( tlv )
            if abs(tree.mcPID[idx]) == 22 :
                if abs(tree.mcMomPID[idx]) == 24 or abs(tree.mcMomPID[idx]) == 11 or abs(tree.mcMomPID[idx]) == 13  or abs(tree.mcMomPID[idx]) == 15   or abs(tree.mcMomPID[idx]) <6  :
                    if tree.mcPt[idx] > photon_pt_cut and math.fabs( tree.mcEta[idx] ) < photon_eta_cut :
                        tlv = ROOT.TLorentzVector()
                        tlv.SetPtEtaPhiE( tree.mcPt[idx], tree.mcEta[idx], tree.mcPhi[idx], tree.mcE[idx] )
                        photons.append( tlv )
            if abs(tree.mcPID[idx]) == 12 or abs(tree.mcPID[idx]) == 14 or abs(tree.mcPID[idx]) == 16 :
                if abs(tree.mcMomPID[idx]) == 24 or abs(tree.mcMomPID[idx]) == 15 :
                    tlv = ROOT.TLorentzVector()
                    tlv.SetPtEtaPhiE( tree.mcPt[idx], tree.mcEta[idx], tree.mcPhi[idx], tree.mcE[idx] )
                    neutrinos.append( tlv )

        met = ROOT.TLorentzVector()
        for neu in neutrinos :
            met += neu

        if len( leptons ) == 1 and len( photons ) == 2 :

            dr_lep_ph1 = leptons[0].DeltaR( photons[0] )
            dr_lep_ph2 = leptons[0].DeltaR( photons[1] )
            dr_ph1_ph2 = photons[0].DeltaR( photons[1] )

            mt_lep_met = calc_mt( leptons[0], met )

            if photons[0].Pt() < lead_photon_pt_cut and photons[1].Pt() < lead_photon_pt_cut : 
                continue
            if dr_lep_ph1 > 0.4 and dr_lep_ph2 > 0.4 and dr_ph1_ph2 > 0.4 and mt_lep_met > 40 :
                n_pass+=1

    return (n_total, n_pass)


def calc_mt( obj, met ) :
    return math.sqrt( 2*obj.Pt()*met.Pt() * ( 1 - math.cos( obj.DeltaPhi(met) ) ) );
                        




def print_events( tree ) :

    for event in range(0,tree.GetEntries()) :
        tree.GetEntry(event)

        print_event( tree )

def print_event( tree ) :

        print 'EVENT'
        for idx in range( 0, tree.nMC ) :
            if abs(tree.mcPID[idx]) == 11 or abs(tree.mcPID[idx]) == 13 :
                print 'LEPTON : pt = %f, eta = %f, phi = %f, PID = %d, MotherPID = %d, stat = %d, parentage = %d ' %(tree.mcPt[idx], tree.mcEta[idx], tree.mcPhi[idx], tree.mcPID[idx],tree.mcMomPID[idx],tree.mcStatus[idx], tree.mcParentage[idx])
            if abs(tree.mcPID[idx]) == 22 :
                print 'PHOTON : pt = %f, eta = %f, phi = %f, PID = %d, MotherPID = %d, stat = %d, parentage = %d ' %(tree.mcPt[idx], tree.mcEta[idx], tree.mcPhi[idx], tree.mcPID[idx],tree.mcMomPID[idx],tree.mcStatus[idx], tree.mcParentage[idx])
            if abs(tree.mcPID[idx]) == 12 or abs(tree.mcPID[idx]) == 14 or abs(tree.mcPID[idx]) == 16 :
                print 'NEUTRINO : pt = %f, eta = %f, phi = %f, PID = %d, MotherPID = %d, stat = %d, parentage = %d ' %(tree.mcPt[idx], tree.mcEta[idx], tree.mcPhi[idx], tree.mcPID[idx],tree.mcMomPID[idx],tree.mcStatus[idx], tree.mcParentage[idx])

            if abs(tree.mcPID[idx]) < 6  :
                print 'QUARK : pt = %f, eta = %f, phi = %f, PID = %d, MotherPID = %d, stat = %d, parentage = %d ' %(tree.mcPt[idx], tree.mcEta[idx], tree.mcPhi[idx], tree.mcPID[idx],tree.mcMomPID[idx],tree.mcStatus[idx], tree.mcParentage[idx])



main()
