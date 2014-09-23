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


def config_analysis( alg_list, args ) :
    """ Configure analysis modules. Order is preserved """

    #files_base = 'root://eoscms//eos/cms/store/user/jkunkle/Samples/MVATrainingSkims/'
    #sig_files = ['job_summer12_gjet_pt20to40_doubleEM.root', 'job_summer12_gjet_pt40_doubleEM.root']
    #bkg_files = ['job_summer12_qcd_pt30to40_doubleEM.root', 'job_summer12_qcd_pt40_doubleEM.root']

    files_base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaForZMva1EleVeto_2014_06_19/'
    sig_dir = ['job_summer12_WAA_ISR', 'job_summer12_Wgg_FSR']
    bkg_dir = ['job_summer12_Zg', 'job_summer12_DYJetsToLL']
    #bkg_dir = ['job_electron_2012a_Jan22rereco', 'job_electron_2012b_Jan22rereco', 'job_electron_2012c_Jan2012rereco', 'job_electron_2012d_Jan22rereco']

    OutputPath = args['outputDir']
    
    sig_files = []
    bkg_files = []
    for dir in sig_dir :
        sig_files += get_files( files_base + dir )
    for dir in bkg_dir :
        bkg_files += get_files( files_base + dir )

    #variables = ['m_lepphph', 'm_lepph1', 'm_lepph2','m_phph', 'leadPhot_leadLepDR', 'sublPhot_leadLepDR', 'ph_phDR', 'dphi_met_lep1', 'dphi_met_ph1', 'dphi_met_ph2',]
    #variables = ['m_lepphph', 'm_lepph1', 'm_lepph2','m_phph', 'leadPhot_leadLepDR', 'sublPhot_leadLepDR', 'ph_phDR']
    #variables = ['mdiff_lepphph_lepph1', 'm_lepph2', 'm_phph', 'leadPhot_leadLepDR', 'sublPhot_leadLepDR', 'ph_phDR', 'm_minZdifflepph']
    vars = ['m_lepphph', 'm_lepph1', 'm_lepph2', 'm_phph', 'leadPhot_leadLepDR', 'sublPhot_leadLepDR', 'ph_phDR']
    vars_dr = ['leadPhot_leadLepDR', 'sublPhot_leadLepDR', 'ph_phDR']

    #alg_list.append(run_mva('ZRejElChMVA3DRVars', sig_files, bkg_files, OutputPath+'trainZRejElCh3DRVars.root', vars_dr, weights='EventWeight', options='nCuts=40:MaxDepth=3' ) )
    alg_list.append(run_mva('ZRejElChMVA7VarsNom', sig_files, bkg_files, OutputPath+'trainZRejElCh7VarsNom.root', vars, weights='EventWeight', options='nCuts=40:MaxDepth=3' ) )

    alg_list.append(run_mva('ZRejElChMVA7VarsVTNorm', sig_files, bkg_files, OutputPath+'trainZRejElCh7VarsVTNorm.root', vars, weights='EventWeight', options='nCuts=40:MaxDepth=3:VarTransform=Norm' ) )
    alg_list.append(run_mva('ZRejElChMVA7VarsVTDeco', sig_files, bkg_files, OutputPath+'trainZRejElCh7VarsVTDeco.root', vars, weights='EventWeight', options='nCuts=40:MaxDepth=3:VarTransform=Deco' ) )
    alg_list.append(run_mva('ZRejElChMVA7VarsVTPCA', sig_files, bkg_files, OutputPath+'trainZRejElCh7VarsVTPCA.root', vars, weights='EventWeight', options='nCuts=40:MaxDepth=3:VarTransform=PCA' ) )
    alg_list.append(run_mva('ZRejElChMVA7VarsVTUniform', sig_files, bkg_files, OutputPath+'trainZRejElCh7VarsVTUniform.root', vars, weights='EventWeight', options='nCuts=40:MaxDepth=3:VarTransform=Uniform' ) )
    alg_list.append(run_mva('ZRejElChMVA7VarsVTGauss', sig_files, bkg_files, OutputPath+'trainZRejElCh7VarsVTGauss.root', vars, weights='EventWeight', options='nCuts=40:MaxDepth=3:VarTransform=Gauss' ) )

def run_mva( job_name, sig_files, bkg_files, outputRootFile, variables, weights=None, options=None, **addtl_vars ) :
    
    module = Filter ( job_name )

    module.add_var( 'JobName', job_name )
    module.add_var( 'SignalFiles', ','.join( sig_files ) )
    module.add_var( 'BackgroundFiles', ','.join( bkg_files ) )
    module.add_var( 'TreeName', 'ggNtuplizer/EventTree' )
    module.add_var( 'OutputFile', outputRootFile)
    module.add_var( 'Variables', ','.join(variables) )
    if weights is not None :
        module.add_var( 'Weights', weights)
    if options is not None :
        module.add_var( 'MvaOptions', options)

    for var, val in addtl_vars.iteritems() :
        module.add_var( var, val )

    #make output directory if necessary
    outputdir = '/'.join( outputRootFile.split('/')[0:-1] )
    if not os.path.isdir( outputdir ) :
        os.makedirs( outputdir )

    return module



