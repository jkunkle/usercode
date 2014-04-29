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

    #files_base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/PhSkimMod_2014_04_15/'
    #sig_dir = ['job_summer12_gjet_pt20to40_doubleEM', 'job_summer12_gjet_pt40_doubleEM']
    #bkg_dir = ['job_summer12_qcd_pt30to40_doubleEM', 'job_summer12_qcd_pt40_doubleEM']

    files_base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/PhMVATraining_2014_04_21/'
    sig_dir = ['job_summer12_Wg']
    bkg_dir = ['job_summer12_Wjets']


    
    sig_files = []
    bkg_files = []
    for dir in sig_dir :
        sig_files += get_files( files_base + dir )
    for dir in bkg_dir :
        bkg_files += get_files( files_base + dir )

    print sig_files
    print bkg_files

    #variables = ['phoR9', 'phoSigmaIEtaIEta', 'phoSigmaIEtaIPhi', 'phoE2x2/phoE5x5', 'phoE1x3/phoE5x5', 'phoE2x5Max/phoE5x5', 'phoSCEtaWidth', 'phoSCPhiWidth', 'phoPFPhoIso', 'phoPFChIso', 'phoPFChIsoWorst']
    variables = ['phoHoverE12', 'phoSigmaIEtaIEta', 'phoPFChIsoPtRhoCorr','phoPFNeuIsoPtRhoCorr', 'phoPFPhoIsoPtRhoCorr' ]

    isovars = ['phoPFChIsoPtRhoCorr','phoPFNeuIsoPtRhoCorr', 'phoPFPhoIsoPtRhoCorr' ]
    idvars2 = ['phoHoverE12', 'phoSigmaIEtaIEta' ]
    #idvars8 = [ 'phoR9', 'phoSigmaIEtaIEta', 'phoSigmaIEtaIPhi', 'phoE2x2/phoE5x5', 'phoE1x3/phoE5x5', 'phoE2x5Max/phoE5x5', 'phoSCEtaWidth', 'phoSCPhiWidth']
    idvars8 = [ 'phoR9', 'phoSigmaIEtaIEta', 'phoSigmaIEtaIPhi', 'phoE2x2/phoE5x5', 'phoE1x3/phoE5x5', 'phoE2x5Max/phoE5x5', 'phoSCEtaWidth', 'phoSCPhiWidth']
    isoidvars = ['phoPFChIsoPtRhoCorr', 'phoSigmaIEtaIEta']

    all_vars = ['ph_r9', 'ph_sigmaIEIE', 'ph_sigmaIEIP', 'ph_s4ratio', 'ph_s13', 'ph_s25', 'ph_SCetaWidth', 'ph_SCphiWidth', 'ph_phoIsoCorr', 'ph_chIsoCorr', 'ph_pfChIsoWorst']


    alg_list.append(run_mva('photonMVAWtrainEE', sig_files, bkg_files, 'trainEE_11varsW.root', all_vars, EtaCut='(ph_eta > -2.5 && ph_eta < -1.566) || (ph_eta > 1.566 && ph_eta < 2.5 )') )
    alg_list.append(run_mva('photonMVAWtrainEB', sig_files, bkg_files, 'trainEB_11varsW.root', all_vars, EtaCut='ph_eta > -1.479 &&  ph_eta < 1.479 ') )

    #alg_list.append(run_mva('photonMVAIsoEE', sig_files, bkg_files, 'trainEE_Isovars.root', isovars, EtaCut='(phoEta > -2.5 && phoEta < -1.566) || (phoEta > 1.566 && phoEta < 2.5 )') )
    #alg_list.append(run_mva('photonMVAIsoEB', sig_files, bkg_files, 'trainEB_Isovars.root', isovars, EtaCut='phoEta > -1.479 &&  phoEta < 1.479 ') )

    #alg_list.append(run_mva('photonMVAId2EE', sig_files, bkg_files, 'trainEE_Id2vars.root', idvars2, EtaCut='(phoEta > -2.5 && phoEta < -1.566) || (phoEta > 1.566 && phoEta < 2.5 )') )
    #alg_list.append(run_mva('photonMVAId2EB', sig_files, bkg_files, 'trainEB_Id2vars.root', idvars2, EtaCut='phoEta > -1.479 &&  phoEta < 1.479 ') )

    #alg_list.append(run_mva('photonMVAId8EE', sig_files, bkg_files, 'trainEE_Id8vars.root', idvars8, EtaCut='(phoEta > -2.5 && phoEta < -1.566) || (phoEta > 1.566 && phoEta < 2.5 )') )
    #alg_list.append(run_mva('photonMVAId8EB', sig_files, bkg_files, 'trainEB_Id8vars.root', idvars8, EtaCut='phoEta > -1.479 &&  phoEta < 1.479 ') )

    #alg_list.append(run_mva('photonMVAIsoIdEE', sig_files, bkg_files, 'trainEE_IdIsovars.root', isoidvars, EtaCut='(phoEta > -2.5 && phoEta < -1.566) || (phoEta > 1.566 && phoEta < 2.5 )') )
    #alg_list.append(run_mva('photonMVAIsoIdEB', sig_files, bkg_files, 'trainEB_IdIsovars.root', isoidvars, EtaCut='phoEta > -1.479 &&  phoEta < 1.479 ') )


def run_mva( job_name, sig_files, bkg_files, outputRootFile, variables, **addtl_vars ) :
    
    module = Filter ( job_name )

    module.add_var( 'JobName', job_name )
    module.add_var( 'SignalFiles', ','.join( sig_files ) )
    module.add_var( 'BackgroundFiles', ','.join( bkg_files ) )
    module.add_var( 'TreeName', 'ggNtuplizer/EventTree' )
    module.add_var( 'OutputFile', '/afs/cern.ch/work/j/jkunkle/private/CMS/MVATraining_2014_04_17/%s' %outputRootFile)
    module.add_var( 'Variables', ','.join(variables) )
    for var, val in addtl_vars.iteritems() :
        module.add_var( var, val )

    return module



