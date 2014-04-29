from core import Filter

def get_remove_filter() :
    """ Define list of regex strings to filter input branches to remove from the output.
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableRemoveFilter on the command line.
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    jet_filt = [
                'jetMVAsExt_full',
                'jetBetaStarCMGExt',
                'jetBetaExt',
                'jetBetaStarClassicExt',
                'jetBetaStar',
                'jetMVAsExt_simple',
                'jetMVAs',
                'jetWPLevelsExt_simple',
                'jetWPLevelsExt_full',
                'jetWPLevelsExt_cutBased',
                'CA8.*',
                'jetLowPt.*',
               ]
    vtx_filt = ['vtx_x', 'vtx_y', 'vtx_z', 'vtxbs_x', 'vtxbs_y', 'vtxbs_z']
    objvtx_filt = ['phoPhiVtx', 'phoEtaVtx', 'phoEtVtx', 'eleEtVtx', 'elePhiVtx', 'eleEtaVtx', 'muEtVtx', 'muPhiVtx', 'muEtaVtx']
    #objvtx_filt = []
    pho_filt = ['phoCiCTrkIsoDR04', 'phoCiCTrkIsoDR03', 'phoCiCPF4chgpfIso04', ]
    tau_filt = ['tau.*']
    
    jet_filt_addtl = [
                'jetDR2Mean',
                #'jetNEF',
                'jetFrac04',
                'jetFrac05',
                'jetFrac03',
                'jetDPhiMETJet',
                'jetFrac02',
                'jetDRMean',
                'jetJECUnc',
                'jetMt',
                'jetRawPt',
                'jetDZ',
                'jetFrac01',
                'jetBetaStarClassic',
                'jetBetaStarCMG',
                'jetBeta',
                #'jetNHF',
                'jetJetBProbabilityBJetTags',
                'jetCombinedSecondaryVtxBJetTags',
                'jetJetProbabilityBJetTags',
                'jetWPLevels',
                'jetMVAsExt_cutBased',
                'jetSoftLeptdR',
                'jetSoftLeptPtRel',
                'jetSoftLeptPt',
                'jetFrac06',
                'jetCEF',
                #'jetNConstituents',
                'jetArea',
                'jetHFEME',
                'jetHFHAE',
                'jetPuJetIdT',
                'jetPuJetIdM',
                'jetPuJetIdL',
                'jetSoftLeptIdEle95',
                'jetFrac07',
                'jetVtx3dL',
                'jetVtx3deL',
                'jetVtxMass',
                'jetSoftLeptIdlooseMu',
                'jetWPLevelsExt_philv1',
                'jetMVAsExt_philv1',
                'jetCombinedSecondaryVtxMVABJetTags',
                'jetPFLooseId',
    ]
    pho_filt_addtl = [
                'phoSeedPhi',
                'phoSeedEta',
                'phoCaloPos_x',
                'phoSCPos_x',
                'phoSCPos_y',
                'phoCaloPos_y',
                'phoSeedTime',
                'phoERight',
                'phoELeft',
                'phoE2x5Left',
                'phoE2x5Right',
                'phoETop',
                'phoEBottom',
                'phoLICTD',
                'phoE2x5Bottom',
                'phoE2x5Top',
                'phoCaloPos_z',
                'phoRegrEerr',
                'phoSCPos_z',
                'phoSeedE',
                'phoCiCPF4phopfIso04',
                'phoSCBrem',
                'phoRegrE',
                'phoSCRPhoIso',
                'phoHcalIsoDR0412',
                #'phoCiCdRtoTrk',
                'phoCrysPhi',
                'phoCrysEta',
                'phoSeedDetId1',
                'phoSeedDetId2',
                'phoCrysIEta',
                #'phoESEffSigmaRR_x',
                'phoESEffSigmaRR_y',
                'phoESEffSigmaRR_z',
                'phoCrysIPhi',
    ]
    ele_filt_addtl = [
                'eleConvDcot',
                'eleSeedPhi',
                'eleSeedEta',
                'eleSeedTime',
                'eleBrem',
                'eleERight',
                'eleE2x5Left',
                'eleELeft',
                'eleE2x5Right',
                'eleETop',
                'eleEBottom',
                'eleE2x5Bottom',
                'eleE2x5Top',
                'elePout',
                'eleModIsoEcal',
                'elePhoRegrEerr',
                'eleSeedE',
                'eleRegrEerr',
                'elePin',
                'eleEcalEn',
                'elePhoRegrE',
                'eleRegrE',
                'eleSCRawEn',
                #'eleIP3D',
                #'eleIP3DErr',
                'eleTrkMomErr',
                'eleCrysPhi',
                'eleCrysEta',
                'eleModIsoHcal',
                'eleModIsoTrk',
                'eleCrysIEta',
                'eleESEn',
                'eleCrysIPhi',
                'eleESEffSigmaRR_x',
                'eleESEffSigmaRR_y',
                'eleESEffSigmaRR_z',
                'eleClass',
                #'eleDzVtx',
                #'eleD0Vtx',
    ]
    conv_filt = [
                'conv.*',
                #'convDxy',
                #'convP4_x',
                #'convP4_y',
                #'convP4_z',
                #'convZofPrimVtxFromTrks',
                #'convDz',
                #'convLz',
                #'convP4_E',
                #'convVtxErr_z',
                #'convVtxErr_x',
                #'convLxy',
                #'convVtxErr_y',
                #'convTk2D0',
                #'convTk2Dz',
                #'convTk2DzErr',
                #'convTk2Pin',
                #'convTk2Pout',
                #'convTk1D0',
                #'convTk1DzErr',
                #'convTk1Dz',
                #'convTk1Pin',
                #'convTk1Pout',
                #'convMVALikelihood',
                #'convValidVtx',
                #'convCh1Ch2',
                #'convChi2Probability',
                #'convRefittedMomentum_x',
                #'convRefittedMomentum_y',
                #'convRefittedMomentum_z',
                #'convPairInvMass',
                'phoConvTrkd0_y',
                'phoConvTrkd0_x',
                'phoConvTrkdz_y',
                'phoConvTrkdz_x',
                'phoConvTrkdzErr_y',
                'phoConvTrkdzErr_x',
                'phoConvLikeLihood',
                'phoConvZofPVfromTrks',
                #'phoPFConvMom_z',
                #'phoPFConvMom_y',
                #'phoPFConvMom_x',
                #'phoPFConvVtx_x',
                #'phoPFConvVtx_y',
                #'phoPFConvVtx_z',
                'phoConvCharge1',
                'phoConvCharge2',
                'phoConvRefittedMomentum_z',
                'phoConvRefittedMomentum_x',
                'phoConvRefittedMomentum_y',
                'phoConvP4_2',
                'phoConvP4_0',
                'phoConvP4_1',
                'phoConvVtxErr_x',
                'phoConvVtxErr_y',
                'phoConvP4_3',
                'phoConvVtxErr_z',
                'phoConvValidVtx',
    ]

    mu_filt_addtl = [
                     'mucktdz',
                     'mucktdxy',
                     'muVtxGlb_z',
                     'mucktPhi',
                     'mucktEta',
                     'muInnerPtErr',
                     #'muIP3D',
                     #'muIP3DErr',
                     'mucktPtErr',
                     'mucktPt',
                     'muVtxGlb_y',
                     'muVtxGlb_x',
                     #'muDzVtx',
                     #'muD0Vtx',
    ]

    met_filt = [ 'trkMET', 'trkMETPhi', 'trkMETx', 'trkMETy'] 

    return (vtx_filt+
           jet_filt+
           objvtx_filt+
           pho_filt+
           tau_filt+
           jet_filt_addtl+
           ele_filt_addtl+
           pho_filt_addtl+
           conv_filt+
           mu_filt_addtl+
           met_filt)

def get_keep_filter() :
    """ Define list of regex strings to filter input branches to retain in the output.  
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableKeepFilter on the command line
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return ['elePt', 'n.*']

def config_analysis( alg_list, args ) :
    """ Configure analysis modules. Order is preserved """

    jet_filt = Filter('FilterJet')
    jet_filt.cut_pt = '> 15'
    alg_list.append(jet_filt)

    #ele_filt = Filter('FilterElec') 
    #ele_filt.cut_pt = '> 10'
    #alg_list.append(ele_filt)

    #mu_filt = Filter('FilterMuon') 
    #mu_filt.cut_pt = '> 10'
    #alg_list.append(mu_filt)

    # should work in general, but only using for diphoton data
    evt_filt = Filter('FilterEvent')
    evt_filt.cut_el_ph_mindr = '< 0.1'
    evt_filt.cut_nMunElOlapPt5 = ' > 0 '
    #evt_filt.add_hist( 'cut_el_ph_mindr', 50, 0, 1 )
    #evt_filt.do_cutflow=True
    

    ##evt_filt.cut_nPho = '> 0'

    alg_list.append(evt_filt)

    trig_filt = Filter('FilterTrigger')
    #trig_filt.cut_trigger = '==1 | ==17 | == 18 | == 19' #diphoton | electron | muon
    #trig_filt.cut_trigger = '==17 | == 18 | == 19' # electron | muon
    #trig_filt.cut_trigger = '== 18 | == 19' #muon
    #trig_filt.cut_trigger = '==17' #electron
    trig_filt.cut_trigger = '==17 | == 18 | == 19 | ==1 | ==4 | == 8 | ==23 | ==48 | ==49 | ==50 | == 51 ' # electron | muon | photon

    alg_list.append(trig_filt)

    #alg_list.append(Filter('CalcLeptonVtxVars'))

