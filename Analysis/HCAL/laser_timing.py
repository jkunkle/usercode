import ROOT

#nominal = '/afs/cern.ch/work/j/jkunkle/private/CMS/HCAL/HBHE_298011.root'
nominal = '/afs/cern.ch/work/j/jkunkle/private/CMS/HCAL/HBHE_297639.root'

modified = '/afs/cern.ch/work/j/jkunkle/private/CMS/HCAL/HBHE_298203.root'



def main() :

    hist_nominal = ROOT.TH1F( 'timing_vs_phi_nominal' , 'timing_vs_phi', 72, 1, 73 )
    hist_modified= ROOT.TH1F( 'timing_vs_phi_modified', 'timing_vs_phi', 72, 1, 73 )

    get_timing_vs_iphi( nominal, hist_nominal )
    get_timing_vs_iphi( modified, hist_modified)

    hist_nominal.SetMarkerColor( ROOT.kBlack) 
    hist_nominal.SetLineColor( ROOT.kBlack) 

    hist_modified.SetMarkerColor( ROOT.kRed) 
    hist_modified.SetLineColor( ROOT.kRed) 

    hist_nominal.Draw()

    hist_modified.Draw('same')

    raw_input('cont')

    ratio = hist_nominal.Clone('ratio')

    ratio.Divide( hist_modified)

    ratio.Draw()

    raw_input('cont')

def get_timing_vs_iphi( fname, outhist ) :

    ofile = ROOT.TFile.Open( fname )

    timing_hists = {}
    for i in range( 1, 73 ) :
        timing_hists[i] = ROOT.TH1F( 'average_timing_iphi%d' %i, 'average_timing_iphi%d' %i, 100, 0, 10 )

    otree = ofile.Get( 'hcalTupleTree/tree' )

    eidx = 0
    for event in otree :

        eidx += 1
        if eidx % 100 == 0 :
            print 'Event ', eidx

        nch = len( otree.HBHEDigiIEta )

        for ich in range( 0, nch ) :

            ieta = otree.HBHEDigiIEta[ich]
            iphi = otree.HBHEDigiIPhi[ich]
            depth = otree.HBHEDigiDepth[ich]

            if depth == 1 and ieta == 1 :

                nts = len(otree.HBHEDigiADC[ich])

                sum_ts_adc = 0
                sum_adc = 0

                for its in range( 0, nts ) :

                    adc = otree.HBHEDigiADC[ich][its]

                    sum_adc += adc
                    sum_ts_adc += its*adc

                timing_hists[iphi].Fill( sum_ts_adc/float(sum_adc) )

    for iphi, hist in timing_hists.iteritems() :

        outhist.SetBinContent(iphi, hist.GetMean() )
        outhist.SetBinError(iphi, hist.GetRMS() )

main()
