import math
import ROOT
import collections

#fname = 'root://eoscms//eos/cms/store/user/ymaravin/MC/LLAA/llaa_nlo_ggNtuple.root'
fname = '/tmp/jkunkle/llaa_nlo_ggNtuple.root'

chain = ROOT.TChain('ggNtuplizer/EventTree')

chain.AddFile( fname )

count_results = collections.OrderedDict()
count_results['total']       = 0
count_results['pt']          = 0
count_results['sceta']       = 0
count_results['sceta']       = 0
count_results['absdEtaIn']   = 0
count_results['absdPhiIn']   = 0
count_results['sigmaIEIE']   = 0
count_results['d0_barrel']   = 0
count_results['z0_barrel']   = 0
count_results['hovere']      = 0
count_results['epdiff']      = 0
count_results['pfIsoCorr30'] = 0
count_results['convfit']     = 0
count_results['misshits']    = 0

def main() :


    evtidx = 0
    for event in chain :

        if evtidx%1000 == 0 :
            print 'On event %d' %evtidx

        evtidx+=1

        for i in range( 0, event.nEle )  :

            EffectiveArea = geteIDEA(event.eleSCEta[i])
            epdiff =  math.fabs(1./event.eleSCEn[i] - event.eleEoverP[i]/event.eleSCEn[i])
            neuiso = event.elePFPhoIso03[i] + event.elePFNeuIso03[i] - EffectiveArea*event.rho2012
            if neuiso < 0 :
                neuiso = 0
            pfiso = (event.elePFChIso03[i] + neuiso)/event.elePt[i]

            increment_counter( 'total' )

            if event.elePt[i] < 10 :
                continue
            if event.elePt[i] > 20 :
                continue

            increment_counter( 'pt' )

            if math.fabs(event.eleSCEta[i]) < 1.479  :

                continue
                increment_counter( 'sceta' )

                if not (math.fabs(event.eledEtaAtVtx[i]) < 0.007) :
                    continue
                increment_counter( 'absdEtaIn' )

                if not (math.fabs(event.eledPhiAtVtx[i]) < 0.15) :
                    continue
                increment_counter( 'absdPhiIn')

                if not (event.eleSigmaIEtaIEta[i] < 0.01) :
                    continue
                increment_counter( 'sigmaIEIE')

                if not (math.fabs(event.eleD0GV[i]) < 0.02) :
                    continue
                increment_counter( 'd0_barrel')

                if not (math.fabs(event.eleDzGV[i]) < 0.2) :
                    continue
                increment_counter( 'z0_barrel')

                if not (event.eleHoverE[i] < 0.12) :
                    continue
                increment_counter( 'hovere')

                if not (epdiff  < 0.05) :
                    continue
                increment_counter( 'epdiff')

                if not (pfiso < 0.15) :
                    continue
                increment_counter( 'pfIsoCorr30')

                if not (event.eleConvVtxFit[i] == 0) :
                    continue
                increment_counter( 'convfit')

                if not (event.eleMissHits[i] <= 1) :
                    continue
                increment_counter( 'misshits')

            else :

                increment_counter( 'sceta' )
                if not (math.fabs(event.eledEtaAtVtx[i]) < 0.009) :
                    continue
                increment_counter( 'absdEtaIn' )

                if not (math.fabs(event.eledPhiAtVtx[i]) < 0.10) :
                    continue
                increment_counter( 'absdPhiIn')

                if not (event.eleSigmaIEtaIEta[i] < 0.03) :
                    continue
                increment_counter( 'sigmaIEIE')

                if not (math.fabs(event.eleD0GV[i]) < 0.02) :
                    continue
                increment_counter( 'd0_barrel')

                if not (math.fabs(event.eleDzGV[i]) < 0.2) :
                    continue
                increment_counter( 'z0_barrel')

                if not (event.eleHoverE[i] < 0.10) :
                    continue
                increment_counter( 'hovere')

                if not (epdiff  < 0.05) :
                    continue
                increment_counter( 'epdiff')

                if event.elePt[i] < 20 :
                    if not (pfiso < 0.10) :
                        continue
                else :
                    if not (pfiso < 0.15) :
                        continue
                increment_counter( 'pfIsoCorr30')

                if not (event.eleConvVtxFit[i] == 0) :
                    continue
                increment_counter( 'convfit')

                if not (event.eleMissHits[i] <= 1) :
                    continue
                increment_counter( 'misshits')


    for key, val in count_results.iteritems() :
        print '%s = %d' %( key, val )


def geteIDEA(SCEta) :
    EffectiveArea = -1;

    if (math.fabs(SCEta) < 1.0 ) :
        EffectiveArea = 0.130; 
    elif (math.fabs(SCEta) >= 1.0   and math.fabs(SCEta) < 1.479 ) :
        EffectiveArea = 0.137;
    elif (math.fabs(SCEta) >= 1.479 and math.fabs(SCEta) < 2.0 ) :
        EffectiveArea = 0.067;
    elif (math.fabs(SCEta) >= 2.0   and math.fabs(SCEta) < 2.2 ) :
        EffectiveArea = 0.089;
    elif (math.fabs(SCEta) >= 2.2   and math.fabs(SCEta) < 2.3 ) :
        EffectiveArea = 0.107;
    elif (math.fabs(SCEta) >= 2.3   and math.fabs(SCEta) < 2.4 ) :
        EffectiveArea = 0.110;
    elif (math.fabs(SCEta) >= 2.4 ) :
        EffectiveArea = 0.138;
    else :
        print 'Wrong eta region'

    return EffectiveArea

def increment_counter( var ) :

    count_results[var] = count_results[var] + 1

main()
