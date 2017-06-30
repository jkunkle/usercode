import os
import ROOT
emap_path = 'http://cmsdoc.cern.ch/cms/HCAL/document/Mapping/Hua/2015-may-4/HCALmapHBEF_G_uHTR.txt'

ROOT.gROOT.SetBatch( True )


fed_colors = {1122 : ROOT.kRed, 1120 : ROOT.kBlue, 1118 : ROOT.kGreen }

def main() :


    emap_file = os.path.basename( emap_path )

    if not os.path.isfile( emap_file ) :
        os.system( 'wget %s' %emap_path )

    ofile = open( emap_file )

    emap_entries = []

    got_header = False

    header_entries = []

    for line in ofile :
        if line[0] == '#' :
            if got_header :
                continue
            else : 
                if line.count( 'file' ) > 0 or line.count('created') > 0 :
                    continue
                else :
                    header_entries = line.split()[1:]
                    got_header = True
                    continue
        else :
            if not got_header :
                print 'Did not get header!  Will not fill data'
                continue
            else :
                channel = {}
                line_entries = line.split()[1:]
                for idx, ent in enumerate(line_entries) :
                    channel[header_entries[idx]] = ent 

                emap_entries.append( channel )

    ofile.close()

    uniq_regions = []

    for ent in emap_entries :

        uniq_regions.append( ent['rbx'] )

    uniq_regions = list( set( uniq_regions) )

    reg_histograms = {}
    reg_crate = {}
    reg_fed = {}
    for ent in emap_entries :

        reg = ent['rbx']

        depth  = int(ent['depth'])
        ieta   = int(ent['eta'])
        side   = int(ent['side'])
        iphi   = int(ent['phi'])
        crate  = int(ent['crate'])
        fed    = int(ent['fedid'])
        slot   = int(ent['uhtr'])
        fib    = int(ent['uhtr_fi'])
        fib_ch = int(ent['fi_ch'])

        ieta = ieta * side

        reg_crate.setdefault( reg, [] )
        reg_fed  .setdefault( reg, [] )

        if crate not in reg_crate[reg] :
            reg_crate[reg].append( crate )
        if fed not in reg_fed[reg] :
            reg_fed[reg].append( fed )

        reg_histograms.setdefault( reg, {} )
        reg_histograms[reg].setdefault( 'depth1', {} )
        reg_histograms[reg].setdefault( 'depth2', {} )
        reg_histograms[reg].setdefault( 'depth3', {} )
        reg_histograms[reg].setdefault( 'fedslot', {} )

        if fed not in reg_histograms[reg]['depth1'].keys() :
            reg_histograms[reg]['depth1'][fed] = ROOT.TH2D( 'depth1_%s_%d'%(reg,fed), 'depth1', 82, -41, 41, 72, 0, 72 )
            reg_histograms[reg]['depth2'][fed] = ROOT.TH2D( 'depth2_%s_%d'%(reg,fed), 'depth2', 82, -41, 41, 72, 0, 72 )
            reg_histograms[reg]['depth3'][fed] = ROOT.TH2D( 'depth3_%s_%d'%(reg,fed), 'depth3', 82, -41, 41, 72, 0, 72 )
            reg_histograms[reg]['fedslot'][fed] = ROOT.TH2D( 'fedslot_%s_%d'%(reg,fed), 'fedslot', 12, 0, 12, 48, 0, 48 )

        bin_val = 1

        depth_name = 'depth%d' %( depth )
        thishist = reg_histograms[reg][depth_name][fed]
        thishist.SetBinContent( thishist.FindBin( ieta, iphi ), bin_val )

        if fib <= 9 :
            fedslot_ybin = (fib - 2)*3 + 1 + fib_ch
        elif fib >= 14 : 
            fedslot_ybin = (fib - 6)*3 + 1 + fib_ch


        reg_histograms[reg]['fedslot'][fed] .SetBinContent( slot, fedslot_ybin, bin_val )

    # histogram formatting
    for reg in uniq_regions :
        for name, fed_hist in reg_histograms[reg].iteritems() :
            for fed, hist in fed_hist.iteritems() :
                hist.SetStats(0)
                fill_color = ROOT.kRed
                if fed in fed_colors :
                    fill_color = fed_colors[fed]

                hist.SetFillColor( fill_color )
                if name == 'fedslot' :
                    for fib_bin in range( 1, 48, 3) :
                        fib_num = (fib_bin + 2)/3 + 1
                        if fib_num > 9 :
                            fib_num += 4
                        hist.GetYaxis().SetBinLabel( fib_bin, '%d-0' %fib_num )

                    for xbin in range( 1, hist.GetNbinsX() +1 ) :
                        hist.GetXaxis().SetBinLabel( xbin, str(xbin) )

                    hist.GetXaxis().SetTitle( 'Slot' )
                    hist.GetYaxis().SetTitle( 'fib-ch' )
                    hist.GetXaxis().SetLabelSize( 0.05 )
                    hist.GetXaxis().SetTitleSize( 0.05 )
                    hist.GetYaxis().SetLabelSize( 0.05 )
                    hist.GetYaxis().SetTitleSize( 0.05 )

                elif name.count( 'depth' ) > 0 :

                    hist.GetXaxis().SetTitle( 'iEta' )
                    hist.GetYaxis().SetTitle( 'iPhi' )
                    hist.GetXaxis().SetLabelSize( 0.05 )
                    hist.GetXaxis().SetTitleSize( 0.05 )
                    hist.GetYaxis().SetLabelSize( 0.05 )
                    hist.GetYaxis().SetTitleSize( 0.05 )

            

        reg_can = ROOT.TCanvas( 'can%s'%reg, 'can%s'%reg, 1200, 300 )
        reg_can.Divide( 4, 1, 0.01, 0.1 )
        move_pad(reg_can.cd(1), y=-0.08 )
        move_pad(reg_can.cd(2), y=-0.08 )
        move_pad(reg_can.cd(3), y=-0.08 )
        move_pad(reg_can.cd(4), y=-0.08 )

        for fidx, fed in enumerate(fed_hist.keys()) :
            draw_opt = 'box'
            if fidx > 0 :
                draw_opt += 'same'
            reg_can.cd(1)
            reg_histograms[reg]['depth1' ][fed].Draw(draw_opt)
            reg_can.cd(2)
            reg_histograms[reg]['depth2' ][fed].Draw(draw_opt)
            reg_can.cd(3)
            reg_histograms[reg]['depth3' ][fed].Draw(draw_opt)
            reg_can.cd(4)
            reg_histograms[reg]['fedslot'][fed].Draw(draw_opt)

        reg_can.cd(0)


        if len( reg_crate[reg] ) == 2 :
            crate_text = 'Crate = #color[%d]{%d}, #color[%d]{%d}' %( fed_colors[reg_fed[reg][0]], reg_crate[reg][0], fed_colors[reg_fed[reg][1]], reg_crate[reg][1] )
            fed_text   = 'FED = #color[%d]{%d}, #color[%d]{%d}' %( fed_colors[reg_fed[reg][0]], reg_fed[reg][0], fed_colors[reg_fed[reg][1]], reg_fed[reg][1] )
        else :
            if reg_fed[reg][0] in fed_colors.keys() :
                color = fed_colors[reg_fed[reg][0]]
            else :
                color = ROOT.kRed
            crate_text = 'Crate = #color[%d]{%d}'  %( color, reg_crate[reg][0] )
            fed_text   = 'FED = #color[%d]{%d}'  %( color, reg_fed[reg][0] )
        text = '%s  -  %s - %s ' %( reg, crate_text, fed_text )

        text = ROOT.TLatex(0.01, 0.9, text )
        text.SetTextSize(0.12) 
        text.Draw()

        reg_can.SaveAs( 'hists_%s.pdf' %reg )


def move_pad( pad, x=0, y=0 ) :


    pad1_x1 = ROOT.Double()
    pad1_x2 = ROOT.Double()
    pad1_y1 = ROOT.Double()
    pad1_y2 = ROOT.Double()

    pad.GetPadPar( pad1_x1, pad1_y1, pad1_x2, pad1_y2 )
    pad.SetPad   ( pad1_x1+x, pad1_y1+y, pad1_x2+x, pad1_y2+y )




main()

