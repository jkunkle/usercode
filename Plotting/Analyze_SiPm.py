import os
import re
import math
import ROOT

from uncertainties import ufloat
from uncertainties import unumpy
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument( '--baseDir', dest='baseDir', default=None, help='Path to input directory' )
parser.add_argument( '--outputDir', dest='outputDir', default=None, help='Directory to save results (will not save if not provided)' )
parser.add_argument( '--fileKey', dest='fileKey', default=None, help='key to match input files' )
parser.add_argument( '--srcCompare', dest='srcCompare', default=False, action='store_true', help='key to match input files' )
parser.add_argument( '--batch', dest='batch', default=False, action='store_true', help='Do not show plots, save without asking' )
parser.add_argument( '--fileList', dest='fileList', default=None, help='Comma separated list of input files' )


options = parser.parse_args()

if options.batch :
    ROOT.gROOT.SetBatch(True)

_leg_entries = { 0 : 'No Source', 1 : 'With Source, Position 1', 2 : 'With Source, Position 2', 3 : 'With Source, Position 3', 4 : 'With Source, Position 4', 5 : 'With Source, Position 5' }

_colors = [ROOT.kBlack, ROOT.kRed, ROOT.kGreen, ROOT.kMagenta, ROOT.kOrange, ROOT.kViolet, ROOT.kGray]

def get_color( index ) :

    if index >= len( _colors ) :
        return ROOT.kBlack
    else :
        return _colors[index]

def main() :

    file_graphs = {}
    file_graphs_dIdVovI = {}
    file_graphs_dVdI = {}
    file_graphs_dlnIdV = {}

    file_graphs_sub = {}
    file_graphs_sub_dIdVovI = {}

    file_list = []
    if options.fileList is not None :
        for split in options.fileList.split(',') :
            file_list.append( split )
    elif options.baseDir is not None :
        for file in os.listdir( options.baseDir ) :
            file_list.append( '%s/%s' %( options.baseDir, file ) )


    selected_files = []
    for file in file_list :
        if file.count('.txt') :
            if options.fileKey is not None :
                if file.count( options.fileKey ) :
                    selected_files.append(file  )
            else :
                selected_files.append( file )

    print selected_files
    file_order = ['']*len(selected_files)

    common_title = ''
    file_is_with_source = {}
    for file in selected_files :
        res = re.match( '.*?/Measurements_for_(.*?)_(\d)_(\d)\.txt', file )
        file_is_with_source[file] = False
        if res is not None :
            common_title = res.group(1)
            src = int(res.group(2))
            pos = int(res.group(3))
            location = 0
            if src == 2 :
                location += 1
                location += (pos-1)
                file_is_with_source[file] = True
            file_order[location] = file

    while '' in file_order : 
        file_order.remove('')

    if not options.srcCompare :
        file_order = selected_files

    print file_order

    file_data = {}
    for idx, file in enumerate(file_order) :
        ofile = open( file, 'r' )

        collected_data = {}

        for line in ofile :
            splitline = line.split()
            collected_data.setdefault( splitline[0], []).append( splitline[1] ) 

        ofile.close()

        # average over currents measured at the same voltage
        file_data[file] = []
        for voltage, currents in collected_data.iteritems() :
            avg = math.fsum( [float(c) for c in currents] )/len(currents)
            stddev = math.sqrt( math.fsum( [ (float(c) - avg)*(float(c) - avg) for c in currents] )/len(currents) )
            file_data[file].append( ( float( voltage),  ufloat( avg , stddev ) ) )

            #if math.fabs(float(voltage)-86) < 0.05 :
            #    print '%f - %e' %( float( voltage), avg )

        file_data[file].sort()

    file_data_diff = {}
    for file in file_order[1:] :
        data_src = file_data[file]
        data_bkg = file_data[file_order[0]]

        file_data_diff[file] = []
        for src, bkg in zip( data_src, data_bkg ) :
            if src[0] != bkg[0] :
                print 'Values should be equal!'
            file_data_diff[file].append( (src[0], src[1]-bkg[1]) )


    for file_idx, file in enumerate(file_order) :
    
        color = get_color( file_idx )
            
        file_graphs[file] = ROOT.TGraphErrors( len(file_data[file]) )
        file_graphs[file].SetName( file )
        file_graphs[file].SetMarkerStyle( 20 )
        file_graphs[file].SetMarkerSize( 1.2 )
        file_graphs[file].SetMarkerColor( color )
        file_graphs[file].SetTitle( 'Measured current for ' + common_title )

        file_graphs_dIdVovI[file] = ROOT.TGraphErrors( len(file_data[file])-1 )
        file_graphs_dIdVovI[file].SetName( file )
        file_graphs_dIdVovI[file].SetMarkerStyle( 20 )
        file_graphs_dIdVovI[file].SetMarkerSize( 1.2 )
        file_graphs_dIdVovI[file].SetMarkerColor( color )
        file_graphs_dIdVovI[file].SetTitle( '(dI/dV)/I for ' + common_title )

        file_graphs_dVdI[file] = ROOT.TGraphErrors( len(file_data[file])-1 )
        file_graphs_dVdI[file].SetName( file )
        file_graphs_dVdI[file].SetMarkerStyle( 20 )
        file_graphs_dVdI[file].SetMarkerSize( 1.2 )
        file_graphs_dVdI[file].SetMarkerColor( color )
        file_graphs_dVdI[file].SetTitle( 'dV/dI for ' + common_title )

        file_graphs_dlnIdV[file] = ROOT.TGraphErrors( len(file_data[file])-1 )
        file_graphs_dlnIdV[file].SetName( file )
        file_graphs_dlnIdV[file].SetMarkerStyle( 20 )
        file_graphs_dlnIdV[file].SetMarkerSize( 1.2 )
        file_graphs_dlnIdV[file].SetMarkerColor( color )
        file_graphs_dlnIdV[file].SetTitle( 'd lnI/dV for ' + common_title )

        #(d( lnI )/dV) ^-1 vs V

        # for making plots with subtracted data
        # ignore the 0th file which is the background
        # measurement
        if file_idx>0 :
            file_graphs_sub[file] = ROOT.TGraphErrors( len(file_data_diff[file]) )
            file_graphs_sub[file].SetName( file )
            file_graphs_sub[file].SetMarkerStyle( 20 )
            file_graphs_sub[file].SetMarkerSize( 1.2 )
            file_graphs_sub[file].SetMarkerColor( color )
            file_graphs_sub[file].SetTitle( 'Background subtracted current for ' + common_title )

            file_graphs_sub_dIdVovI[file] = ROOT.TGraphErrors( len(file_data_diff[file])-1 )
            file_graphs_sub_dIdVovI[file].SetName( file )
            file_graphs_sub_dIdVovI[file].SetMarkerStyle( 20 )
            file_graphs_sub_dIdVovI[file].SetMarkerSize( 1.2 )
            file_graphs_sub_dIdVovI[file].SetMarkerColor( color )
            file_graphs_sub_dIdVovI[file].SetTitle( 'Background subtracted (dI/dV)/I for ' + common_title )

            # fill graphs with subtracted data
            # data[0] is voltage data[1] is current difference
            for idx, data in enumerate(file_data_diff[file]) :
                file_graphs_sub[file].SetPoint( idx, data[0], data[1] )

            for idx, lower_data in enumerate(file_data_diff[file][:-1]) :
                upper_data = file_data_diff[file][idx+1]
                avg_voltage = (lower_data[0] + upper_data[0] )/2.
                avg_current = (lower_data[1] + upper_data[1] )/2.

                delta_voltage = upper_data[0] - lower_data[0]
                delta_current = upper_data[1] - lower_data[1]

                x_point_dIdVovI = avg_voltage
                y_point_dIdVovI = ( delta_current / delta_voltage ) / avg_current 
                file_graphs_sub_dIdVovI[file].SetPoint( idx, x_point_dIdVovI, y_point_dIdVovI )

        # fill graphs with raw data
        # data[0] is voltage data[1] is current
        for idx, data in enumerate(file_data[file]) :
            file_graphs[file].SetPoint( idx, data[0], data[1].n )
            file_graphs[file].SetPointError( idx, 0, data[1].s )

        # get two data points for derivatives. lower_data is the
        # lower voltage and upper_data is the next voltage point
        # data[0] is the voltage and data[1] is the current
        for idx, lower_data in enumerate(file_data[file][:-1]) :
            upper_data = file_data[file][idx+1]

            avg_voltage = (lower_data[0] + upper_data[0] )/2.
            avg_current = (lower_data[1] + upper_data[1] )/2.

            delta_voltage = upper_data[0] - lower_data[0]
            delta_current = upper_data[1] - lower_data[1]
            delta_ln_current = unumpy.log( upper_data[1] ) - unumpy.log( lower_data[1] )
            #delta_ln_current = math.log( upper_data[1] - lower_data[1] )

            x_point_dIdVovI = avg_voltage
            y_point_dIdVovI = ( delta_current / delta_voltage ) / avg_current 
            file_graphs_dIdVovI[file].SetPoint( idx, x_point_dIdVovI, y_point_dIdVovI.n )
            file_graphs_dIdVovI[file].SetPointError( idx, 0, y_point_dIdVovI.s )

            x_point_dVdI = avg_voltage
            y_point_dVdI = ( delta_voltage / delta_current ) 
            file_graphs_dVdI[file].SetPoint( idx, x_point_dVdI, y_point_dVdI.n )
            file_graphs_dVdI[file].SetPointError( idx, 0, y_point_dVdI.s )

            x_point_dlnIdV = avg_voltage
            y_point_dlnIdV = 1.0/( delta_ln_current / delta_voltage )
            file_graphs_dlnIdV[file].SetPoint( idx, x_point_dlnIdV, y_point_dlnIdV.n )
            file_graphs_dlnIdV[file].SetPointError( idx, 0, y_point_dlnIdV.s )


    c1 = ROOT.TCanvas('c1', 'c1')

    leg_I_vs_V = None
    leg_dIdVovI_vs_V = None
    leg_dVdI_vs_V = None
    leg_dlnIdV_vs_V = None
    leg_sub_I_vs_V = None
    leg_sub_dIdVovI_vs_V = None

    if len( file_order ) <= len(_leg_entries) :
        leg_I_vs_V           = ROOT.TLegend(0.12, 0.55, 0.42, 0.85)
        leg_dIdVovI_vs_V     = ROOT.TLegend(0.12, 0.55, 0.42, 0.85)
        leg_dVdI_vs_V        = ROOT.TLegend(0.2, 0.25, 0.5, 0.55)
        leg_dlnIdV_vs_V      = ROOT.TLegend(0.68, 0.6, 0.95, 0.85)
        leg_sub_I_vs_V       = ROOT.TLegend(0.12, 0.55, 0.42, 0.85)
        leg_sub_dIdVovI_vs_V = ROOT.TLegend(0.12, 0.55, 0.42, 0.85)

        leg_I_vs_V           .SetFillColor( ROOT.kWhite )
        leg_dIdVovI_vs_V     .SetFillColor( ROOT.kWhite )
        leg_dVdI_vs_V        .SetFillColor( ROOT.kWhite )
        leg_dlnIdV_vs_V      .SetFillColor( ROOT.kWhite )
        leg_sub_I_vs_V       .SetFillColor( ROOT.kWhite )
        leg_sub_dIdVovI_vs_V .SetFillColor( ROOT.kWhite )

        for idx, file in enumerate(file_order) :
            leg_I_vs_V.           AddEntry(file_graphs[file],  _leg_entries[idx], 'PE' )
            leg_dIdVovI_vs_V     .AddEntry(file_graphs[file],  _leg_entries[idx], 'PE' )
            leg_dVdI_vs_V        .AddEntry(file_graphs[file],  _leg_entries[idx], 'PE' )
            leg_dlnIdV_vs_V      .AddEntry(file_graphs[file],  _leg_entries[idx], 'PE' )
            if idx > 0 :
                leg_sub_I_vs_V       .AddEntry(file_graphs[file],  _leg_entries[idx], 'PE' )
                leg_sub_dIdVovI_vs_V .AddEntry(file_graphs[file],  _leg_entries[idx], 'PE' )
                

    for idx, file in enumerate(file_order) :
        if idx == 0 :
            file_graphs[file].Draw('AP')
            file_graphs[file].GetXaxis().SetTitle('Bias Voltage')
        else :
            file_graphs[file].Draw('Psame')

    if leg_I_vs_V is not None :
        leg_I_vs_V.Draw()

    c1.SetLogy()

    c2 = ROOT.TCanvas('c2', 'c2')
    for idx, file in enumerate(file_order) :
        if idx == 0 :
            file_graphs_dIdVovI[file].Draw('AP')
            file_graphs_dIdVovI[file].GetXaxis().SetTitle('Bias Voltage')
        else :
            file_graphs_dIdVovI[file].Draw('Psame')

    if leg_dIdVovI_vs_V is not None :
        leg_dIdVovI_vs_V.Draw()

    c3 = ROOT.TCanvas('c3', 'c3')
    for idx, file in enumerate(file_order) :
        if idx == 0 :
            file_graphs_dVdI[file].Draw('AP')
            file_graphs_dVdI[file].GetXaxis().SetTitle('Bias Voltage')
        else :
            file_graphs_dVdI[file].Draw('Psame')

    if leg_dVdI_vs_V is not None :
        leg_dVdI_vs_V.Draw()
    c3.SetLogy()

    c4 = ROOT.TCanvas('c4', 'c4')
    for idx, file in enumerate(file_order) :
        if idx == 0 :
            file_graphs_dlnIdV[file].Draw('AP')
            file_graphs_dlnIdV[file].GetXaxis().SetTitle('Bias Voltage')
            file_graphs_dlnIdV[file].SetMaximum(1.5)
        else :
            file_graphs_dlnIdV[file].Draw('Psame')

    if leg_dlnIdV_vs_V is not None :
        leg_dlnIdV_vs_V.Draw()

    c5 = ROOT.TCanvas('c5', 'c5')
    for idx, file in enumerate(file_order) :
        if idx == 0 :
            continue
        elif idx == 1 :
            file_graphs_sub[file].Draw('AP')
            file_graphs_sub[file].GetXaxis().SetTitle('Bias Voltage')
        else :
            file_graphs_sub[file].Draw('Psame')

    c5.SetLogy()
    if leg_sub_I_vs_V is not None :
        leg_sub_I_vs_V.Draw()

    c6 = ROOT.TCanvas('c6', 'c6')
    for idx, file in enumerate(file_order) :
        if idx == 0 :
            continue
        elif idx == 1 :
            file_graphs_sub_dIdVovI[file].Draw('AP')
            file_graphs_sub_dIdVovI[file].GetXaxis().SetTitle('Bias Voltage')
        else :
            file_graphs_sub_dIdVovI[file].Draw('Psame')

    if leg_sub_dIdVovI_vs_V is not None :
        leg_sub_dIdVovI_vs_V.Draw()

    if not options.batch :
        raw_input('cont')

    if options.outputDir is not None :
        save = 'n'
        if options.batch :
            save = 'y'
        else :
            save = raw_input('save ? (y/n)' )
        if save == 'y' :
            if not os.path.isdir( options.outputDir ) :
                os.makedirs( options.outputDir )
            c1.SaveAs( '%s/Results_I_vs_V_%s.pdf' %(options.outputDir, common_title ))
            c2.SaveAs( '%s/Results_dIdVovI_vs_V_%s.pdf' %(options.outputDir, common_title ))
            c3.SaveAs( '%s/Results_dVdI_vs_V_%s.pdf' %(options.outputDir, common_title ))
            c4.SaveAs( '%s/Results_dlnIdV_vs_V_%s.pdf' %(options.outputDir, common_title ))
            c5.SaveAs( '%s/Results_sub_I_vs_V_%s.pdf' %(options.outputDir, common_title ))
            c6.SaveAs( '%s/Results_sub_dIdVovI_vs_V_%s.pdf' %(options.outputDir, common_title ))

main()



