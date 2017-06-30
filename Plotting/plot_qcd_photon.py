import ROOT
import math
fname = '/data/users/jkunkle/Samples/Trigger//RecoOutput/QCD/Job_0000/ntuple_QCD.root'

ofile = ROOT.TFile.Open( fname )
ofile.ls()

otree = ofile.Get('tupel/EventTree' )

for br in otree.GetListOfBranches() :
    if br.GetName().count('ph_' ) :
        print br.GetName()

hist_sigmaIEIEAll = ROOT.TH1F( 'hist_sigmaIEIEAll', 'hist_sigmaIEIEAll', 50, 0, 0.05 )
hist_chHadIsoAll = ROOT.TH1F( 'hist_chHadIsoAll', 'hist_chHadIsoAll', 50, 0, 20 )

hist_sigmaIEIECut = ROOT.TH1F( 'hist_sigmaIEIECut', 'hist_sigmaIEIECut', 50, 0, 0.05 )
hist_chHadIsoCut = ROOT.TH1F( 'hist_chHadIsoCut', 'hist_chHadIsoCut', 50, 0, 20 )


idx = 0
for event in otree :

    idx += 1

    if idx % 100 == 0 :
        print 'Event ', idx

    for iph in range( 0, otree.ph_n ) :

        if otree.ph_passHOverEMedium[iph] and math.fabs(otree.ph_eta[iph]) < 1.4 :
            hist_sigmaIEIEAll.Fill( otree.ph_sigmaIEIE[iph] )
            hist_chHadIsoAll.Fill( otree.ph_chIsoCorr[iph] )

            if otree.ph_phoIso[iph] < 6 :
                hist_chHadIsoCut.Fill( otree.ph_chIsoCorr[iph] )
                hist_sigmaIEIECut.Fill( otree.ph_sigmaIEIE[iph] )



hist_sigmaIEIECut.SetLineColor( ROOT.kRed )
hist_sigmaIEIEAll.SetLineColor( ROOT.kBlack )
hist_sigmaIEIEAll.GetXaxis().SetTitle('Sigma i#eta i#eta' )
hist_sigmaIEIECut.GetXaxis().SetTitle('Sigma i#eta i#eta' )

hist_chHadIsoAll.GetXaxis().SetTitle('Charged Hadron Isolation' )
hist_chHadIsoCut.GetXaxis().SetTitle('Charged Hadron Isolation' )

hist_chHadIsoCut.SetLineColor( ROOT.kRed )
hist_chHadIsoAll.SetLineColor( ROOT.kBlack )

hist_sigmaIEIEAll.DrawNormalized()
hist_sigmaIEIECut.DrawNormalized('same')
raw_input('cont')
hist_chHadIsoAll.DrawNormalized()
hist_chHadIsoCut.DrawNormalized('same')
raw_input('cont')





