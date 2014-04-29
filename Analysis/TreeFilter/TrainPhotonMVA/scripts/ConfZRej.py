from core import Filter
import os

def get_remove_filter() :
    """ Define list of regex strings to filter input branches to remove from the output.
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableRemoveFilter on the command line.
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return []

def get_keep_filter() :
    """ Define list of regex strings to filter input branches to retain in the output.  
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableKeepFilter on the command line
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return []

def get_files( top_dir ) :

    output = []

    for top, dirs, files in os.walk( top_dir ) :
        for file in files : 
            if file == 'tree.root' :
                output.append(top + '/' + file )

    return output


def config_analysis( alg_list ) :
    """ Configure analysis modules. Order is preserved """

    #files_base = 'root://eoscms//eos/cms/store/user/jkunkle/Samples/MVATrainingSkims/'
    #sig_files = ['job_summer12_gjet_pt20to40_doubleEM.root', 'job_summer12_gjet_pt40_doubleEM.root']
    #bkg_files = ['job_summer12_qcd_pt30to40_doubleEM.root', 'job_summer12_qcd_pt40_doubleEM.root']

    files_base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVarForMVA_2014_04_29/'
    sig_dir = ['job_summer12_WAA_ISR', 'job_summer12_Wgg_FSR']
    bkg_dir = ['job_summer12_Zg']

    OutputPath = '/afs/cern.ch/work/j/jkunkle/private/CMS/MVATrainingZRej_2014_04_29/'
    
    sig_files = []
    bkg_files = []
    for dir in sig_dir :
        sig_files += get_files( files_base + dir )
    for dir in bkg_dir :
        bkg_files += get_files( files_base + dir )

    #variables = ['m_lepphph', 'm_lepph1', 'm_lepph2','m_phph', 'leadPhot_leadLepDR', 'sublPhot_leadLepDR', 'ph_phDR', 'dphi_met_lep1', 'dphi_met_ph1', 'dphi_met_ph2',]
    #variables = ['m_lepphph', 'm_lepph1', 'm_lepph2','m_phph', 'leadPhot_leadLepDR', 'sublPhot_leadLepDR', 'ph_phDR']
    #variables = ['mdiff_lepphph_lepph1', 'm_lepph2', 'm_phph', 'leadPhot_leadLepDR', 'sublPhot_leadLepDR', 'ph_phDR', 'm_minZdifflepph']
    variables = ['m_lepphphMod', 'm_lepph1Mod', 'm_lepph2Mod', 'm_phph', 'leadPhot_leadLepDR', 'sublPhot_leadLepDR', 'ph_phDR']

    #alg_list.append(run_mva('ZRej7VarNom', sig_files, bkg_files, OutputPath+'trainZRejTEST.root', variables, weights='EventWeight', EtaCut='el_passtrig_n>0 && el_n==1 && ph_n==2 && leadPhot_pt>15 && sublPhot_pt>15 && ph_passMedium ') )
    alg_list.append(run_mva('ZRejElChMVA7VarsMod40Cuts', sig_files, bkg_files, OutputPath+'trainZRejElCh7varsMod40Cuts.root', variables, weights='EventWeight', EtaCut='el_passtrig_n>0 && el_n==1 && ph_n==2 && leadPhot_pt>15 && sublPhot_pt>15 && ph_passMedium ') )
    #alg_list.append(run_mva('ZRejMuChMVA7VarsNom', sig_files, bkg_files, OutputPath+'trainZRejMuCh7varsNom.root', variables, weights='EventWeight', EtaCut='mu_passtrig_n>0 && mu_n==1 && ph_n==2 && leadPhot_pt>15 && sublPhot_pt>15 && ph_passMedium ') )

    #alg_list.append(run_mva('photonMVAIsoEE', sig_files, bkg_files, 'trainEE_Isovars.root', isovars, EtaCut='(phoEta > -2.5 && phoEta < -1.566) || (phoEta > 1.566 && phoEta < 2.5 )') )
    #alg_list.append(run_mva('photonMVAIsoEB', sig_files, bkg_files, 'trainEB_Isovars.root', isovars, EtaCut='phoEta > -1.479 &&  phoEta < 1.479 ') )

    #alg_list.append(run_mva('photonMVAId2EE', sig_files, bkg_files, 'trainEE_Id2vars.root', idvars2, EtaCut='(phoEta > -2.5 && phoEta < -1.566) || (phoEta > 1.566 && phoEta < 2.5 )') )
    #alg_list.append(run_mva('photonMVAId2EB', sig_files, bkg_files, 'trainEB_Id2vars.root', idvars2, EtaCut='phoEta > -1.479 &&  phoEta < 1.479 ') )

    #alg_list.append(run_mva('photonMVAId8EE', sig_files, bkg_files, 'trainEE_Id8vars.root', idvars8, EtaCut='(phoEta > -2.5 && phoEta < -1.566) || (phoEta > 1.566 && phoEta < 2.5 )') )
    #alg_list.append(run_mva('photonMVAId8EB', sig_files, bkg_files, 'trainEB_Id8vars.root', idvars8, EtaCut='phoEta > -1.479 &&  phoEta < 1.479 ') )

    #alg_list.append(run_mva('photonMVAIsoIdEE', sig_files, bkg_files, 'trainEE_IdIsovars.root', isoidvars, EtaCut='(phoEta > -2.5 && phoEta < -1.566) || (phoEta > 1.566 && phoEta < 2.5 )') )
    #alg_list.append(run_mva('photonMVAIsoIdEB', sig_files, bkg_files, 'trainEB_IdIsovars.root', isoidvars, EtaCut='phoEta > -1.479 &&  phoEta < 1.479 ') )


def run_mva( job_name, sig_files, bkg_files, outputRootFile, variables, weights=None, **addtl_vars ) :
    
    module = Filter ( job_name )

    module.add_var( 'JobName', job_name )
    module.add_var( 'SignalFiles', ','.join( sig_files ) )
    module.add_var( 'BackgroundFiles', ','.join( bkg_files ) )
    module.add_var( 'TreeName', 'ggNtuplizer/EventTree' )
    module.add_var( 'OutputFile', outputRootFile)
    module.add_var( 'Variables', ','.join(variables) )
    if weights is not None :
        module.add_var( 'Weights', weights)

    for var, val in addtl_vars.iteritems() :
        module.add_var( var, val )

    #make output directory if necessary
    outputdir = '/'.join( outputRootFile.split('/')[0:-1] )
    if not os.path.isdir( outputdir ) :
        os.makedirs( outputdir )

    return module



