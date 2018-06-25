import ROOT

file_path = '/afs/cern.ch/work/j/jkunkle/private/CMS/HCAL/Laser_MinimumBias_296950.root'
tree_name = 'hcalTupleTree/tree'

_NTS_HBHE = 10
_NTS_HF   = 3

def main() :

    ofile = ROOT.TFile.Open( file_path, 'READ' )

    otree = ofile.Get( tree_name )

    nevt = otree.GetEntries()

    hist_avg_adc_hbhe = ROOT.TH1F( 'hist_avg_adc_hbhe', 'hist_avg_adc_hbhe', nevt, 0, nevt )
    hist_avg_adc_hf = ROOT.TH1F( 'hist_avg_adc_hf', 'hist_avg_adc_hf', nevt, 0, nevt )

    ievt = 0

    for event in otree :

        ievt += 1

        if ievt %100 == 0 :
            print 'Event ', ievt

        sumadc_hbhe = 0
        nch_hbhe = len(otree.HBHEDigiIEta)

        for ich in range( 0, nch_hbhe ) :

            for its in range( 0, _NTS_HBHE ) :

                sumadc_hbhe += otree.HBHEDigiADC[ich][its]


        sumadc_hf = 0
        nch_hf = len(otree.QIE10DigiIEta)

        for ich in range( 0, nch_hf ) :

            for its in range( 0, _NTS_HF ) :

                sumadc_hf += otree.QIE10DigiADC[ich][its]

        hist_avg_adc_hbhe.SetBinContent( ievt, sumadc_hbhe / float( nch_hbhe ) )
        hist_avg_adc_hf.SetBinContent( ievt, sumadc_hf / float( nch_hf ) )


    hist_avg_adc_hbhe.Draw()
    raw_input('cont')
    hist_avg_adc_hf.Draw()
    raw_input('cont')










main()


