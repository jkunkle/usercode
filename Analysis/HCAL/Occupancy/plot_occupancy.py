#run 282092
import ROOT

#115-125, 423-433, 732-742, 1041-1051, 1350-1360, 1659-1669, 1968-1978, 2276-2286
#hb_occupancy = [ (41, 984), (33, 895), (30, 845), ( 26, 802 ), (23, 764), ( 21, 737 ), (18.5, 712), ( 17, 699 ) ]
#he_occupancy = [ (41, 1188), (33, 1074), (30, 998), ( 26, 928 ), (23, 862), ( 21, 809 ), (18.5, 759), ( 17, 706 ) ]
hb_occupancy = [ (41, 984), (33, 895), (30, 845), ( 26, 802 ), (23, 764), ( 21, 737 ), (18.5, 712), ( 17, 699 ) ]
he_occupancy = [ (41, 1188), (33, 1074), (30, 998), ( 26, 928 ), (23, 862), ( 21, 809 ), (18.5, 759), ( 17, 706 ) ]

data_volume = [ (41, 4.72), (33, 4.3), (30, 4.06), ( 26, 3.83 ), (23, 3.62), ( 21, 3.46 ), (18.5, 3.31), ( 17, 3.18 ) ]


graph_hb = ROOT.TGraph( len( hb_occupancy ) )
graph_he = ROOT.TGraph( len( he_occupancy ) )
graph_vol = ROOT.TGraph( len( data_volume) )


for idx, val in enumerate(hb_occupancy) :
    graph_hb.SetPoint( idx, val[0], val[1] )
for idx, val in enumerate(he_occupancy) :
    graph_he.SetPoint( idx, val[0], val[1] )
for idx, val in enumerate(data_volume) :
    graph_vol.SetPoint( idx, val[0], val[1] )


graph_hb.SetMarkerStyle( 20 )
graph_he.SetMarkerStyle( 20 )
graph_vol.SetMarkerStyle( 20 )


myf_hb = ROOT.TF1( 'fit_hb', '[0] + [1]*x', 15, 50 )
myf_he = ROOT.TF1( 'fit_he', '[0] + [1]*x', 15, 50 )
myf_vol = ROOT.TF1( 'fit_vol', '[0] + [1]*x', 15, 50 )

myf_hb.SetParameter( 0, 500 )
myf_hb.SetParameter( 1, 12 )
myf_he.SetParameter( 0, 500 )
myf_he.SetParameter( 1, 12 )
myf_vol.SetParameter( 0, 2 )
myf_vol.SetParameter( 1, 0.2 )

graph_hb.Fit( myf_hb )
graph_he.Fit( myf_he )
graph_vol.Fit( myf_vol )

can_hb = ROOT.TCanvas( 'HB', 'HB' )

graph_hb.Draw('AP')
myf_hb.Draw('same')

raw_input('cont')

can_he = ROOT.TCanvas( 'HE', 'HE' )

graph_he.Draw('AP')
myf_he.Draw('same')

raw_input('cont')

can_vol = ROOT.TCanvas( 'DataVolume', 'DataVolume' )

graph_vol.Draw('AP')
myf_vol.Draw('same')

raw_input('cont')

graph_hb.GetXaxis().SetTitle( 'Pileup multiplicity' )
graph_hb.GetYaxis().SetTitle( 'Occupancy' )
graph_he.GetXaxis().SetTitle( 'Pileup multiplicity' )
graph_he.GetYaxis().SetTitle( 'Occupancy' )
graph_vol.GetXaxis().SetTitle( 'Pileup multiplicity' )
graph_vol.GetYaxis().SetTitle( 'Data size (kb / event )' )

graph_hb.SetTitle('')
graph_he.SetTitle('')
graph_vol.SetTitle('')

print ' HB occupancy at 100 PU = ', myf_hb.Eval( 100 )
print ' HE occupancy at 100 PU = ', myf_he.Eval( 100 )
print ' Data volume 100 PU = ', myf_vol.Eval( 100 )

can_hb.SaveAs( 'hb_occupancy.pdf' )
can_he.SaveAs( 'he_occupancy.pdf' )
can_vol.SaveAs( 'data_volume.pdf' )


