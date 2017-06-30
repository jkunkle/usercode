import ROOT

filename1 = '/home/jkunkle/usercode/Analysis/TreeFilter/RecoTrig17/TEST/Job_0000/ntuple_GGG.root'
filename2 = '/data/users/jkunkle/Trigger/hltbits_processed_GGG.root'

treename1 = 'tupel/EventTree'
treename2 = 'HltTree'

ofile1 = ROOT.TFile.Open( filename1 )
ofile2 = ROOT.TFile.Open( filename2 )

otree1 = ofile1.Get(treename1)
otree2 = ofile2.Get(treename2)

print otree1.GetEntries()
print otree2.GetEntries()

for br in otree1.GetListOfBranches() :
    print br.GetName()

print '-----------------------------------------'

for br in otree2.GetListOfBranches() :
    print br.GetName()

hist_nocut = ROOT.TH1D( 'hist_nocut', 'hist_nocut', 2, 0, 2 )
hist_cut = ROOT.TH1D( 'hist_cut', 'hist_cut', 2, 0, 2 )

#idx = 0
#trig_indices = {}
#for br in otree2.GetListOfBranches() :
#    if br.GetName().count('HLT') :
#        trig_indices[br.GetName()] = idx
#        idx += 1
#
#result_map = {}

#for event in otree2 :
#
#    result_list = [0]*len(trig_indices) 
#
#    for trig, idx in trig_indices.iteritems() :
#        result_list[idx] = getattr(otree2, trig)
#
#    result_map[otree2.Event] = result_list

hists = {}
for trig in trig_indices.keys() :
    hists[trig+'nocut'] = ROOT.TH1D( 'hist_%s_nocut'%trig, 'hist_%s_nocut' %trig, 2, 0, 2 )
    hists[trig+'cut'] = ROOT.TH1D( 'hist_%s_cut'%trig, 'hist_%s_cut' %trig, 2, 0, 2 )

    hists[trig+'HEall'] = ROOT.TH1F( 'hist_%s_HEall'%trig, 'hist_%s_HEall' %trig, 50, 0, 1 )
    hists[trig+'HEcut'] = ROOT.TH1F( 'hist_%s_HEcut'%trig, 'hist_%s_HEcut' %trig, 50, 0, 1 )

    hists[trig+'HEall'] = ROOT.TH1F( 'hist_%s_HEall'%trig, 'hist_%s_HEall' %trig, 50, 0, 1 )
    hists[trig+'HEcut'] = ROOT.TH1F( 'hist_%s_HEcut'%trig, 'hist_%s_HEcut' %trig, 50, 0, 1 )

for event in otree1 :

    event_num = otree1.EvtNum

    #print result_map[event_num]
    for trig, idx in trig_indices.iteritems() :
        hists[trig+'nocut'].Fill( result_map[event_num][idx] )

        for phidx in range( 0, otree1.ph_n ) :
            hists[trig+'HEall'].Fill( otree1.ph_HoverE[phidx] )

            if result_map[event_num][idx] :
                hists[trig+'HEcut'].Fill( otree1.ph_HoverE[phidx] )


    if otree1.ph_n < 3 :
        continue

    ptlead = otree1.ph_pt[0]
    ptsubl = otree1.ph_pt[1]
    ptthrl = otree1.ph_pt[2]

    if ptlead > 35 and ptsubl > 25 and ptthrl > 25 :
        for trig, idx in trig_indices.iteritems() :
            hists[trig+'cut'].Fill( result_map[event_num][idx] )

        #if result_map[event_num][trig_indices['HLT_TriPhoton20NonIso_v0']] and not result_map[event_num][trig_indices['HLT_TriPhoton302020NonIso_v0']] :
        #    print 'Bad  : Photon pts = %f, %f, %f' %( ptlead, ptsubl, ptthrl )
        #else :
        #    print 'Good : Photon pts = %f, %f, %f' %( ptlead, ptsubl, ptthrl )

for trig in trig_indices.keys() :

    npass_before = hists[trig+'nocut'].GetBinContent(2)
    npass_after  = hists[trig+'cut'].GetBinContent(2)

    tot_before = hists[trig+'nocut'].Integral()
    tot_after = hists[trig+'cut'].Integral()
    
    print trig
    print 'Before pass = %d, tot = %d, frac = %f ' %( npass_before,  tot_before, float( npass_before/tot_before) )
    print 'After pass = %d, tot = %d, frac = %f ' %( npass_after,  tot_after, float( npass_after/tot_after ) )

    hists[trig+'HEcut'].SetLineColor( ROOT.kRed )
    hists[trig+'HEall'].SetLineColor( ROOT.kBlack )

    hists[trig+'HEall'].DrawNormalized()
    hists[trig+'HEcut'].DrawNormalized('same')
    raw_input('cont')

    print '----------------------------------'

