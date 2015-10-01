import xml.dom.minidom as dom
# versions of python at P5 tend to be older
# therefore use optparse instead of argparse
import time
import getpass
import os
import re
from optparse import OptionParser


def main() :

    parser = OptionParser()
    
    parser.add_option( '--inputFile' , dest='inputFile' , help='Path to input file' )
    parser.add_option( '--outputDir' , dest='outputDir' , help='Path of output directory' )
    
    parser.add_option( '--HCALGains'            , dest='HCALGains'            , default=False, action='store_true', help='Write HCALGains xml'            )
    parser.add_option( '--HCALChannelQuality'   , dest='HCALChannelQuality'   , default=False, action='store_true', help='Write HCALChannelQuality xml'   )
    parser.add_option( '--HCALElectronicsMap'   , dest='HCALElectronicsMap'   , default=False, action='store_true', help='Write HCALElectronicsMap xml'   )
    parser.add_option( '--HCALL1TriggerObjects' , dest='HCALL1TriggerObjects' , default=False, action='store_true', help='Write HCALL1TriggerObjects xml' )
    parser.add_option( '--HCALLongRecoParams'   , dest='HCALLongRecoParams'   , default=False, action='store_true', help='Write HCALLongRecoParams xml'   )
    parser.add_option( '--HCALLUTCorrs'         , dest='HCALLUTCorrs'         , default=False, action='store_true', help='Write HCALLUTCorrs xml'         )
    parser.add_option( '--HCALLUTMetaData'      , dest='HCALLUTMetaData'      , default=False, action='store_true', help='Write HCALLUTMetaData xml'      )
    parser.add_option( '--HCALMCParams'         , dest='HCALMCParams'         , default=False, action='store_true', help='Write HCALMCParams xml'         )
    parser.add_option( '--HCALPedestals'        , dest='HCALPedestals'        , default=False, action='store_true', help='Write HCALPedestals xml'        )
    parser.add_option( '--HCALPedestalWidths'   , dest='HCALPedestalWidths'   , default=False, action='store_true', help='Write HCALPedestalWidths xml'   )
    parser.add_option( '--HCALPFCorrs'          , dest='HCALPFCorrs'          , default=False, action='store_true', help='Write HCALPFCorrs xml'          )
    parser.add_option( '--HCALRecoParams'       , dest='HCALRecoParams'       , default=False, action='store_true', help='Write HCALRecoParams xml'       )
    parser.add_option( '--HCALRespCorrs'        , dest='HCALRespCorrs'        , default=False, action='store_true', help='Write HCALRespCorrs xml'        )
    parser.add_option( '--HCALTimeCorrs'        , dest='HCALTimeCorrs'        , default=False, action='store_true', help='Write HCALTimeCorrs xml'        )
    parser.add_option( '--HCALZSThresholds'     , dest='HCALZSThresholds'     , default=False, action='store_true', help='Write HCALZSThresholds xml'     )
    
    (options, args) = parser.parse_args()


    if options.HCALGains :
        MakeHCALGainsXML( options.inputFile, options.outputDir )
    if options.HCALChannelQuality :
        MakeHCALChannelQualityXML( options.inputFile, options.outputDir )
    if options.HCALElectronicsMap:
        MakeHCALElectronicsMapXML( options.inputFile, options.outputDir )
    if options.HCALL1TriggerObjects:
        MakeHCALL1TriggerObjectsXML( options.inputFile, options.outputDir )
    if options.HCALLongRecoParams:
        MakeHCALLongRecoParamsXML( options.inputFile, options.outputDir )
    if options.HCALLUTCorrs :
        MakeHCALLUTCorrsXML( options.inputFile, options.outputDir )
    if options.HCALLUTMetaData:
        MakeHCALLUTMetaDataXML( options.inputFile, options.outputDir )
    if options.HCALMCParams:
        MakeHCALMCParamsXML( options.inputFile, options.outputDir )
    if options.HCALPedestals:
        MakeHCALPedestalsXML( options.inputFile, options.outputDir )
    if options.HCALPedestalWidths:
        MakeHCALPedestalWidthsXML( options.inputFile, options.outputDir )
    if options.HCALPFCorrs:
        MakeHCALPFCorrsXML( options.inputFile, options.outputDir )
    if options.HCALRecoParams:
        MakeHCALRecoParamsXML( options.inputFile, options.outputDir )
    if options.HCALRespCorrs:
        MakeHCALRespCorrsXML( options.inputFile, options.outputDir )
    if options.HCALTimeCorrs:
        MakeHCALTimeCorrsXML( options.inputFile, options.outputDir )
    if options.HCALZSThresholds:
        MakeHCALZSThresholdsXML( options.inputFile, options.outputDir )

def ParseFileName( fpath, basename ) :

    info = {}

    fname = os.path.basename( fpath )
    dirname = fpath.split('/')[-2]

    # match the directory to the expected basename
    # extract the version and any other info at the end
    res_dir = re.match( '%s_v(\d+)\.(\d+)_(\w+)' %basename, dirname )

    res_nov = None
    if res_dir is None :
        # some directories do not have a version 
        # if the previous match did not work, try 
        # without a version
        res_nov = re.match('%s_(\w+)' %basename, dirname )
        if res_nov is None :
            print 'Could not parse file %s using basename %s' %(dirname,basename)
            return info

    res_file = re.match( 'IOV(\d+)\.txt', fname )
    if res_file is None :
        print 'Could not parse file name %s' %fname
        return info

    #-----------------------------------
    # Get detector name
    # The regex match for the name 
    # should be passed as the 'basename'
    # argument.  If a file may contain either
    # HCAL or ZDC one should pass as basename
    # '(HCAL|ZDC)RemainerOfName'
    #-----------------------------------
    det = None
    if basename.lower().count('hcal') : 
        det = 'HCAL'
    elif basename.lower().count('zdc') : 
        det = 'ZDC'

    # parse the tag out of the
    # directory name
    if res_dir is not None :
        version = '%s.%s' %( res_dir.group(1), res_dir.group(2) )
        type = res_dir.group(3)
        tag = '%s_v%s_%s' %( res_dir.group(1), version, type )
    elif res_nov is not None :
        tag = '%s_%s' %(basename,res_nov.group(1))

    # get the run number from the file name
    run_number = res_file.group(1)
    run_name = str(run_number)

    # for now the comment is just the tag
    comment = tag

    info['det'] = det
    info['run_name'] = run_name
    info['tag'] = tag
    info['comment'] = comment

    return info

def MakeHCALZSThresholdsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'value', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False
    #det_name, run_name, tag_name, comment = ParseFileName( input_file, 'HcalZSThresholds' )
    
    info = ParseFileName( input_file, 'HcalZSThresholds' )

    if not info :
        return False

    config_name = 'HCAL_ZERO_SUPPRESSION_TYPE01'
    long_name = 'HCAL zero suppression [type 1]' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            value_ele = create_element_with_text(doc, 'ZERO_SUPPRESSION', channel_data['value'] )
            data_ele.appendChild( value_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALTimeCorrsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'value', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalTimeCorrs' )

    if not info :
        return False

    config_name = 'HCAL_TIME_CORRECTIONS'
    long_name = 'HCAL Time Corrections' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            value_ele = create_element_with_text(doc, 'VALUE', channel_data['value'] )
            data_ele.appendChild( value_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALRespCorrsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'value', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalRespCorrs' )

    if not info :
        return False

    config_name = 'HCAL_RESPONSE_CORRECTIONS_V1'
    long_name = 'HCAL Response corrections [V1]' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            value_ele = create_element_with_text(doc, 'VALUE', channel_data['value'] )
            data_ele.appendChild( value_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALRecoParamsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'param1', 'param2', 'DetId', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'det', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    # don't return on fail
    # because we expect to miss one column in the header
    #if not success :
    #    return False

    info = ParseFileName( input_file, 'HcalRecoParams' )

    if not info :
        return False

    config_name = 'HCAL_RECO_PARAMS'
    long_name = 'HCAL Reconstruction Parameters' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            param1_ele = create_element_with_text(doc, 'PARAM1', channel_data['param1'] )
            data_ele.appendChild( param1_ele )

            param2_ele = create_element_with_text(doc, 'PARAM2', channel_data['param2'] )
            data_ele.appendChild( param2_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            corrphase_ele = create_element_with_text(doc, 'CORR_PHAS_CNTMNT', channel_data['a0'] )
            data_ele.appendChild( corrphase_ele )

            corrlead_ele = create_element_with_text(doc, 'CORR_LEAD_EDGE', channel_data['a1'] )
            data_ele.appendChild( corrlead_ele )

            corxnphase_ele = create_element_with_text(doc, 'CORXN_PHASE_NS', channel_data['a2'] )
            data_ele.appendChild( corxnphase_ele )

            firstsamp_ele = create_element_with_text(doc, 'FIRST_SAMPLE', channel_data['a3'] )
            data_ele.appendChild( firstsamp_ele )

            sampstoadd_ele = create_element_with_text(doc, 'SAMPLS_TO_ADD', channel_data['a4'] )
            data_ele.appendChild( sampstoadd_ele )

            pulseshape_ele = create_element_with_text(doc, 'PULSE_SHAPE_ID', channel_data['a5'] )
            data_ele.appendChild( pulseshape_ele )

            useleak_ele = create_element_with_text(doc, 'USE_LEAK_CORRXN', channel_data['b0'] )
            data_ele.appendChild( useleak_ele )

            leakcorrxn_ele = create_element_with_text(doc, 'LEAK_CORRXN_ID', channel_data['b1'] )
            data_ele.appendChild( leakcorrxn_ele )

            corrtimeslew_ele = create_element_with_text(doc, 'CORR_TIME_SLEW', channel_data['b2'] )
            data_ele.appendChild( corrtimeslew_ele )

            timeslepcorxn_ele = create_element_with_text(doc, 'TIME_SLEW_CORXN_ID', channel_data['b3'] )
            data_ele.appendChild( timeslepcorxn_ele )

            corrtiming_ele = create_element_with_text(doc, 'CORR_TIMING', channel_data['b4'] )
            data_ele.appendChild( corrtiming_ele )

            firstaux_ele = create_element_with_text(doc, 'FIRST_AUX_TS', channel_data['b5'] )
            data_ele.appendChild( firstaux_ele )

            spclcase_ele = create_element_with_text(doc, 'SPCL_CASE_ID', channel_data['b6'] )
            data_ele.appendChild( spclcase_ele )

            noiseflag_ele = create_element_with_text(doc, 'NOISE_FLAG_ID', channel_data['b7'] )
            data_ele.appendChild( noiseflag_ele )

            pileup_ele = create_element_with_text(doc, 'PILEUP_CLEAN_ID', channel_data['b8'] )
            data_ele.appendChild( pileup_ele )

            packing_ele = create_element_with_text(doc, 'PACK_SCHEME', channel_data['addtl1'] )
            data_ele.appendChild( packing_ele )

            # --------------------------
            # END DATA
            # --------------------------

            data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALPFCorrsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'value', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalPFCorrs' )

    if not info :
        return False

    config_name = 'HCAL_PF_CORRECTIONS'
    long_name = 'HCAL PF Corrections' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )


        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            value_ele = create_element_with_text(doc, 'VALUE', channel_data['value'] )
            data_ele.appendChild( value_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALPedestalWidthsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'cov_0_0', 'cov_0_1', 'cov_0_2', 'cov_0_3', 'cov_1_0', 'cov_1_1', 'cov_1_2', 'cov_1_3', 'cov_2_0', 'cov_2_1', 'cov_2_2', 'cov_2_3', 'cov_3_0', 'cov_3_1', 'cov_3_2', 'cov_3_3', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalPedestalWidths_ADC' )

    if not info :
        return False

    config_name = 'HCAL_PEDESTAL_WIDTHS_V3'
    long_name = 'HCAL Pedestal Widths [V3]' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            cov00_ele = create_element_with_text(doc, 'COVARIANCE_00', channel_data['cov_0_0'] )
            data_ele.appendChild( cov00_ele )

            cov01_ele = create_element_with_text(doc, 'COVARIANCE_01', channel_data['cov_0_1'] )
            data_ele.appendChild( cov01_ele )

            cov02_ele = create_element_with_text(doc, 'COVARIANCE_02', channel_data['cov_0_2'] )
            data_ele.appendChild( cov02_ele )

            cov03_ele = create_element_with_text(doc, 'COVARIANCE_03', channel_data['cov_0_3'] )
            data_ele.appendChild( cov03_ele )

            cov10_ele = create_element_with_text(doc, 'COVARIANCE_10', channel_data['cov_1_0'] )
            data_ele.appendChild( cov10_ele )

            cov11_ele = create_element_with_text(doc, 'COVARIANCE_11', channel_data['cov_1_1'] )
            data_ele.appendChild( cov11_ele )

            cov12_ele = create_element_with_text(doc, 'COVARIANCE_12', channel_data['cov_1_2'] )
            data_ele.appendChild( cov12_ele )

            cov13_ele = create_element_with_text(doc, 'COVARIANCE_13', channel_data['cov_1_3'] )
            data_ele.appendChild( cov13_ele )

            cov20_ele = create_element_with_text(doc, 'COVARIANCE_20', channel_data['cov_2_0'] )
            data_ele.appendChild( cov20_ele )

            cov21_ele = create_element_with_text(doc, 'COVARIANCE_21', channel_data['cov_2_1'] )
            data_ele.appendChild( cov21_ele )

            cov22_ele = create_element_with_text(doc, 'COVARIANCE_22', channel_data['cov_2_2'] )
            data_ele.appendChild( cov22_ele )

            cov23_ele = create_element_with_text(doc, 'COVARIANCE_23', channel_data['cov_2_3'] )
            data_ele.appendChild( cov23_ele )

            cov30_ele = create_element_with_text(doc, 'COVARIANCE_30', channel_data['cov_3_0'] )
            data_ele.appendChild( cov30_ele )

            cov31_ele = create_element_with_text(doc, 'COVARIANCE_31', channel_data['cov_3_1'] )
            data_ele.appendChild( cov31_ele )

            cov32_ele = create_element_with_text(doc, 'COVARIANCE_32', channel_data['cov_3_2'] )
            data_ele.appendChild( cov32_ele )

            cov33_ele = create_element_with_text(doc, 'COVARIANCE_33', channel_data['cov_3_3'] )
            data_ele.appendChild( cov33_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALPedestalsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'cap0', 'cap1', 'cap2', 'cap3', 'widthcap0', 'widthcap1', 'widthcap2', 'widthcap3', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalPedestals_ADC' )

    if not info :
        return False

    config_name = 'HCAL_DETMON_PEDESTALS_V1'
    long_name = 'HCAL Pedestals [abort gap global]' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            mean0_ele = create_element_with_text(doc, 'MEAN0', channel_data['cap0'] )
            data_ele.appendChild( mean0_ele )

            mean1_ele = create_element_with_text(doc, 'MEAN1', channel_data['cap1'] )
            data_ele.appendChild( mean1_ele )

            mean2_ele = create_element_with_text(doc, 'MEAN2', channel_data['cap2'] )
            data_ele.appendChild( mean2_ele )

            mean3_ele = create_element_with_text(doc, 'MEAN3', channel_data['cap3'] )
            data_ele.appendChild( mean3_ele )

            rms0_ele = create_element_with_text(doc, 'RMS0', channel_data['widthcap0'] )
            data_ele.appendChild( rms0_ele )

            rms1_ele = create_element_with_text(doc, 'RMS1', channel_data['widthcap1'] )
            data_ele.appendChild( rms1_ele )

            rms2_ele = create_element_with_text(doc, 'RMS2', channel_data['widthcap2'] )
            data_ele.appendChild( rms2_ele )

            rms3_ele = create_element_with_text(doc, 'RMS3', channel_data['widthcap3'] )
            data_ele.appendChild( rms3_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALLUTMetaDataXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'Rcalib', 'LutGranularity', 'OutputLutThreshold', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalLutMetadata' )

    if not info :
        return False

    config_name = 'HCAL_LUT_CHAN_DATA_V1'
    long_name = 'Hcal LUT Channel Data [type 1]' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            rec_ele = create_element_with_text(doc, 'REC_HIT_CALIBRATION', channel_data['Rcalib'] )
            data_ele.appendChild( rec_ele )

            gran_ele = create_element_with_text(doc, 'LUT_GRANULARITY', channel_data['LutGranularity'] )
            data_ele.appendChild( gran_ele )

            thresh_ele = create_element_with_text(doc, 'OUTPUT_LUT_THRESHOLD', channel_data['OutputLutThreshold'] )
            data_ele.appendChild( thresh_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALMCParamsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'param1', 'DetId', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalMCParams' )

    if not info :
        return False

    config_name = 'HCAL_MONTE_CARLO_PARAMS'
    long_name = 'HCAL Monte Carlo Parameters' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            param_ele = create_element_with_text(doc, 'PARAM1', channel_data['param1'] )
            data_ele.appendChild( param_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            shape_ele = create_element_with_text(doc, 'SIGNAL_SHAPE', channel_data['a0'] )
            data_ele.appendChild( shape_ele )

            sync_ele = create_element_with_text(doc, 'SYNC_PHASE', channel_data['a1'] )
            data_ele.appendChild( sync_ele )

            bin_ele = create_element_with_text(doc, 'BIN_OF_MAX', channel_data['a2'] )
            data_ele.appendChild( bin_ele )

            phase_ele = create_element_with_text(doc, 'TIME_PHASE', channel_data['a3'] )
            data_ele.appendChild( phase_ele )

            phase_ele = create_element_with_text(doc, 'TIME_SMEAR', channel_data['a4'] )
            data_ele.appendChild( phase_ele )

            pack_ele = create_element_with_text(doc, 'PACK_SCHEME', channel_data['a5'] )
            data_ele.appendChild( pack_ele )

            # --------------------------
            # END DATA
            # --------------------------

            data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALLUTCorrsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'value', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalLUTCorrs' )

    if not info :
        return False

    config_name = 'HCAL_LUT_CORRECTIONS'
    long_name = 'HCAL LUT Corrections' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            value_ele = create_element_with_text(doc, 'VALUE', channel_data['value'] )
            data_ele.appendChild( value_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALLongRecoParamsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'signalTSs', 'noiseTSs', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalLongRecoParams' )

    if not info :
        return False

    config_name = 'ZDC_LONG_RECO_PARAMS'
    long_name = 'ZDC Long Reconstruction Parameters' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            signalTSs = channel_data['signalTSs'].split(',')
            noiseTSs = channel_data['noiseTSs'].split(',')

            if len( signalTSs ) > 0 :
                sts4_ele = create_element_with_text(doc, 'SGNL_TS4', signalTSs[0] )
                data_ele.appendChild( sts4_ele )

            if len( signalTSs ) > 1 :
                sts5_ele = create_element_with_text(doc, 'SGNL_TS5', signalTSs[1] )
                data_ele.appendChild( sts5_ele )

            if len( signalTSs ) > 2 :
                sts6_ele = create_element_with_text(doc, 'SGNL_TS6', signalTSs[2] )
                data_ele.appendChild( sts6_ele )

            if len( noiseTSs ) > 0 :
                nts1_ele = create_element_with_text(doc, 'NOISE_TS1', noiseTSs[0] )
                data_ele.appendChild( nts1_ele )

            if len( noiseTSs ) > 1 :
                nts2_ele = create_element_with_text(doc, 'NOISE_TS2', noiseTSs[1] )
                data_ele.appendChild( nts2_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            # --------------------------
            # END DATA
            # --------------------------

            data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALL1TriggerObjectsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'ped', 'respcorrgain', 'flag', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalL1TriggerObjects' )

    if not info :
        return False

    config_name = 'HCAL_L1_TRIGGER_OBJECTS_V1'
    long_name = 'HCAL L1 Trigger Objects [V1]' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            ped_ele = create_element_with_text(doc, 'AVERAGE_PEDESTAL', channel_data['ped'] )
            data_ele.appendChild( ped_ele )

            gain_ele = create_element_with_text(doc, 'RESPONSE_CORRECTED_GAIN', channel_data['respcorrgain'] )
            data_ele.appendChild( gain_ele )

            flag_ele = create_element_with_text(doc, 'FLAG', channel_data['flag'] )
            data_ele.appendChild( flag_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALElectronicsMapXML( input_file, output_dir ) :

    required_columns = ['i', 'cr', 'sl', 'tb', 'dcc', 'spigot', 'fiber/slb', 'fibcha/slbcha', 'subdet', 'ieta', 'iphi', 'depth']

    file_data = ReadFile( input_file, 'subdet' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalElectronicsMap' )

    if not info :
        return False

    config_name = 'HCAL_EMAP'
    long_name = 'HCAL e-map' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            detid_ele = create_element_with_text(doc, 'DETID', channel_data['i'] )
            data_ele.appendChild( detid_ele )

            cr_ele = create_element_with_text(doc, 'CR', channel_data['cr'] )
            data_ele.appendChild( cr_ele )

            sl_ele = create_element_with_text(doc, 'SL', channel_data['sl'] )
            data_ele.appendChild( sl_ele )

            tb_ele = create_element_with_text(doc, 'TB', channel_data['tb'] )
            data_ele.appendChild( tb_ele )

            dcc_ele = create_element_with_text(doc, 'DCC', channel_data['dcc'] )
            data_ele.appendChild( dcc_ele )

            spigot_ele = create_element_with_text(doc, 'SPIGOT', channel_data['spigot'] )
            data_ele.appendChild( spigot_ele )

            fiber_ele = create_element_with_text(doc, 'FIBER', channel_data['fiber/slb'] )
            data_ele.appendChild( fiber_ele )

            fiberchan_ele = create_element_with_text(doc, 'FIBERCHAN', channel_data['fibcha/slbcha'] )
            data_ele.appendChild( fiberchan_ele )

            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['subdet'], eta=channel_data['ieta'], channel=channel_data['iphi'] )
            elif data_type == 'HT' :
                data_set = MakeHTDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, eta=channel_data['ieta'], phi=channel_data['iphi'], subdet=channel_data['subdet'] )
            elif data_type == 'CALIB' :
                data_set = MakeCALIBDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, eta=channel_data['ieta'], phi=channel_data['iphi'], subdet=channel_data['subdet'], type=channel_data['depth'] )

            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['ieta'], iphi=channel_data['iphi'], depth=channel_data['depth'], subdet=channel_data['subdet'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALChannelQualityXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', '(base)' ,'value', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalChannelQuality' )

    if not info :
        return False

    config_name = 'HCAL_CHANNEL_QUALITY_V2'
    long_name = 'HCAL Channel Quality [V2]' 

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            status_ele = create_element_with_text(doc, 'CHANNEL_STATUS_HEX', channel_data['value'] )
            data_ele.appendChild( status_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )


            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )

        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True

def MakeHCALGainsXML( input_file, output_dir ) :

    required_columns = ['eta', 'phi', 'dep', 'det', 'cap0' ,'cap1', 'cap2', 'cap3', 'cap4', 'DetId']

    file_data = ReadFile( input_file, 'det' )

    success = check_input_compatibility( file_data.values()[0], required_columns, input_file )

    if not success :
        return False

    info = ParseFileName( input_file, 'HcalGains' )

    if not info :
        return False

    config_name = 'HCAL_INVERSE_GAINS_V1'
    long_name = 'HCAL Inverse Gains [V1]'

    for data_type, input_data in file_data.iteritems() :

        output_file = '%s_%s_%s.xml' %( data_type, info['comment'], info['run_name'] )

        #doc = dom.Document(version='1.0', standalone='yes')
        doc = dom.Document()

        root = MakeStandardHeader( doc, table_name=config_name, long_name=long_name, run_name=info['run_name'], tag_name=info['tag'], detector_name=input_data.detector_name, comment=info['comment'], channelmap=input_data.channelmap )

        for channel_data in input_data.loop_entries() :

            # --------------------------
            # BEGIN DATA
            # holds cap data
            # --------------------------
            data_ele = doc.createElement( 'DATA' )

            cap0_ele = create_element_with_text(doc, 'CAP0', channel_data['cap0'] )
            data_ele.appendChild( cap0_ele )

            cap1_ele = create_element_with_text(doc, 'CAP1', channel_data['cap1'] )
            data_ele.appendChild( cap1_ele )

            cap2_ele = create_element_with_text(doc, 'CAP2', channel_data['cap2'] )
            data_ele.appendChild( cap2_ele )

            cap3_ele = create_element_with_text(doc, 'CAP3', channel_data['cap3'] )
            data_ele.appendChild( cap3_ele )

            detid_ele = create_element_with_text(doc, 'HCALDETID', channel_data['DetId'] )
            data_ele.appendChild( detid_ele )

            # --------------------------
            # END DATA
            # --------------------------

            if data_type == 'ZDC' :
                data_set = MakeZDCDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, section=channel_data['det'], eta=channel_data['eta'], channel=channel_data['phi'] )
            else :
                data_set = MakeStandardDataSet( doc, data_ele, comment=info['comment'], table_name=input_data.channelmap, ieta=channel_data['eta'], iphi=channel_data['phi'], depth=channel_data['dep'], subdet=channel_data['det'] )
            root.appendChild( data_set )
            
        # --------------------------
        # END ROOT
        # --------------------------

        WriteStandardOutput( doc, '%s/%s' %(output_dir, output_file ) )

    return True
    
def MakeStandardHeader( doc, table_name, long_name, run_name=None, tag_name=None, detector_name='HCAL', comment='', channelmap='HCAL_CHANNELS' ) :

    # --------------------------
    # BEGIN ROOT 
    # Encloses entire document
    # --------------------------
    root = doc.createElement('ROOT')
    doc.appendChild(root)

    # --------------------------
    # BEGIN HEADER
    # Encloses just names and run
    # --------------------------
    header = doc.createElement( 'HEADER' )
    root.appendChild(header)

    # --------------------------
    # BEGIN TYPE
    # Encloses just names
    # --------------------------
    type = doc.createElement( 'TYPE' )
    header.appendChild(type)

    # name of DB table
    tab_name_ele = create_element_with_text(doc, 'EXTENSION_TABLE_NAME', table_name)
    type.appendChild(tab_name_ele)

    # name with type included
    long_name_ele = create_element_with_text(doc, 'NAME', long_name )
    type.appendChild(long_name_ele)

    # --------------------------
    # END TYPE
    # --------------------------

    # --------------------------
    # BEGIN RUN
    # if the run is None then the run
    # entry should just say no-run
    # otherwise make an entry for the run
    # --------------------------
    if len(run_name) < 2 :
        run_ele = create_element_with_attrs( doc, 'RUN', {'mode' : 'no-run'} )
    else :
        run_ele = doc.createElement( 'RUN' )
        run_name_ele = create_element_with_text(doc, 'RUN_NAME', run_name )
        run_ele.appendChild( run_name_ele )
    header.appendChild( run_ele )
    # --------------------------
    # END RUN
    # --------------------------
    hints_ele = create_element_with_attrs( doc, 'HINTS', {'channelmap' : channelmap } )
    header.appendChild( hints_ele )
    # --------------------------
    # END HEADER
    # --------------------------

    # --------------------------
    # BEGIN ELEMENTS
    # Holds some addtl info
    # --------------------------
    elements = doc.createElement( 'ELEMENTS' )
    root.appendChild(elements)

    # add <DATA_SET id="-1"/> -- unknown functionality
    data_set = create_element_with_attrs( doc, 'DATA_SET', {'id' : '-1' } )
    elements.appendChild( data_set )

    # --------------------------
    # BEGIN IOV
    # set id to 1 -- unknown functionality
    # holds intervals (defaut to 1, -1 )
    # --------------------------
    iov = create_element_with_attrs( doc, 'IOV', {'id' : '1'} )
    elements.appendChild(iov)

    if run_name is None :
        begin_entry = '1'
    else :
        begin_entry = run_name

    iov_begin = create_element_with_text(doc, 'INTERVAL_OF_VALIDITY_BEGIN', begin_entry )
    iov_end   = create_element_with_text(doc, 'INTERVAL_OF_VALIDITY_END', '-1' )

    iov.appendChild(iov_begin)
    iov.appendChild(iov_end)
    # --------------------------
    # END IOV
    # --------------------------

    # --------------------------
    # BEGIN TAG
    # set id=2, mode=auto -- unknown functionality
    # holds tag, detector, comment
    # --------------------------
    tag = create_element_with_attrs( doc, 'TAG', {'id' : '2','mode' : 'auto'  } )
    elements.appendChild(tag)

    tag_name = create_element_with_text(doc, 'TAG_NAME', tag_name )
    det_name = create_element_with_text(doc, 'DETECTOR_NAME', detector_name )
    comment  = create_element_with_text(doc, 'COMMENT_DESCRIPTION',comment )

    tag.appendChild(tag_name)
    tag.appendChild(det_name)
    tag.appendChild(comment)

    # --------------------------
    # END TAG
    # --------------------------
    # --------------------------
    # END ELEMENTS
    # --------------------------

    # --------------------------
    # BEGIN MAPS
    # holds some unknown info
    # --------------------------
    maps = doc.createElement( 'MAPS' )
    root.appendChild(maps)

    # --------------------------
    # BEGIN TAG
    # holds some unknown info
    # add <TAG idref="2"> -- unknown functionality
    # --------------------------
    maps_tag = create_element_with_attrs(doc, 'TAG', {'idref' : '2'} )
    maps.appendChild(maps_tag)

    # --------------------------
    # BEGIN IOV
    # holds some unknown info
    # add <IOV idref="1"> -- unknown functionality
    # --------------------------
    maps_iov = create_element_with_attrs(doc, 'IOV', {'idref' : '1'} )
    maps_tag.appendChild( maps_iov )

    # add <DATA_SET idref="-1"/> -- unknown functionality
    maps_data_set = create_element_with_attrs(doc, 'DATA_SET', {'idref' : '-1'} )
    maps_iov.appendChild( maps_data_set )
    # --------------------------
    # END IOV
    # --------------------------
    # --------------------------
    # END TAG
    # --------------------------
    # --------------------------
    # END MAPS
    # --------------------------

    return root

def MakeStandardDataSet( doc, data_element, comment, table_name, ieta, iphi, depth, subdet ) :

    data_set = MakeStandardDataSetHeader( doc, comment )

    MakeStandardDataSetChannel( doc, data_set, data_element, table_name, ieta, iphi, depth, subdet )

    return data_set

def MakeZDCDataSet( doc, data_element, comment, table_name, section, eta, channel ) :

    data_set = MakeStandardDataSetHeader( doc, comment )

    MakeZDCDataSetChannel( doc, data_set, data_element, table_name, section, eta, channel )

    return data_set

def MakeCALIBDataSet( doc, data_element, comment, table_name, eta, phi, type, subdet) :

    data_set = MakeStandardDataSetHeader( doc, comment )

    MakeCALIBDataSetChannel( doc, data_set, data_element, table_name, eta, phi, type, subdet )

    return data_set

def MakeHTDataSet( doc, data_element, comment, table_name, eta, phi, subdet) :

    data_set = MakeStandardDataSetHeader( doc, comment )

    MakeHTDataSetChannel( doc, data_set, data_element, table_name, eta, phi, subdet )

    return data_set

def MakeStandardDataSetChannel( doc, data_set, data_element, table_name, ieta, iphi, depth, subdet ) :
    
    # --------------------------
    # BEGIN CHANNEL
    # holds channel location
    # --------------------------
    
    channel_ele = doc.createElement( 'CHANNEL' )
    data_set.appendChild( channel_ele )

    ext_table_ele = create_element_with_text(doc, 'EXTENSION_TABLE_NAME', table_name )
    channel_ele.appendChild( ext_table_ele )

    subdet_ele = create_element_with_text(doc, 'SUBDET', subdet )
    channel_ele.appendChild( subdet_ele )

    ieta_ele = create_element_with_text(doc, 'IETA', ieta )
    channel_ele.appendChild( ieta_ele )

    iphi_ele = create_element_with_text(doc, 'IPHI', iphi )
    channel_ele.appendChild( iphi_ele )

    depth_ele = create_element_with_text(doc, 'DEPTH', depth )
    channel_ele.appendChild( depth_ele )

    # --------------------------
    # END CHANNEL
    # --------------------------
    
    data_set.appendChild( data_element )
    # --------------------------
    # END DATA_SET
    # --------------------------

def MakeZDCDataSetChannel( doc, data_set, data_element, table_name, section, eta, channel ) :
    
    if int(eta) > 0 :
        isposeta = '1'
    else :
        isposeta = '0'

    section_name = section.split('_')[1]

    # --------------------------
    # BEGIN CHANNEL
    # holds channel location
    # --------------------------
    
    top_channel_ele = doc.createElement( 'CHANNEL' )
    data_set.appendChild( top_channel_ele )

    ext_table_ele = create_element_with_text(doc, 'EXTENSION_TABLE_NAME', table_name )
    top_channel_ele.appendChild( ext_table_ele )

    section_ele = create_element_with_text(doc, 'SECTION', section_name )
    top_channel_ele.appendChild( section_ele )

    isposeta_ele = create_element_with_text(doc, 'ISPOSITIVEETA', isposeta )
    top_channel_ele.appendChild( isposeta_ele )

    channel_ele = create_element_with_text(doc, 'CHANNEL', channel )
    top_channel_ele.appendChild( channel_ele )

    # --------------------------
    # END CHANNEL
    # --------------------------
    
    data_set.appendChild( data_element )
    # --------------------------
    # END DATA_SET
    # --------------------------

def MakeCALIBDataSetChannel( doc, data_set, data_element, table_name, ieta, iphi, type, subdet ) :

    subdet_name = subdet.split('_')[-1]
    
    # --------------------------
    # BEGIN CHANNEL
    # holds channel location
    # --------------------------
    
    channel_ele = doc.createElement( 'CHANNEL' )
    data_set.appendChild( channel_ele )

    ext_table_ele = create_element_with_text(doc, 'EXTENSION_TABLE_NAME', table_name )
    channel_ele.appendChild( ext_table_ele )

    subdet_ele = create_element_with_text(doc, 'SUBDET', subdet_name )
    channel_ele.appendChild( subdet_ele )

    ieta_ele = create_element_with_text(doc, 'IETA', ieta )
    channel_ele.appendChild( ieta_ele )

    iphi_ele = create_element_with_text(doc, 'IPHI', iphi )
    channel_ele.appendChild( iphi_ele )

    depth_ele = create_element_with_text(doc, 'TYPE', type )
    channel_ele.appendChild( depth_ele )

    # --------------------------
    # END CHANNEL
    # --------------------------
    
    data_set.appendChild( data_element )
    # --------------------------
    # END DATA_SET
    # --------------------------


def MakeHTDataSetChannel( doc, data_set, data_element, table_name, ieta, iphi, subdet ) :

    # --------------------------
    # BEGIN CHANNEL
    # holds channel location
    # --------------------------
    
    channel_ele = doc.createElement( 'CHANNEL' )
    data_set.appendChild( channel_ele )

    ext_table_ele = create_element_with_text(doc, 'EXTENSION_TABLE_NAME', table_name )
    channel_ele.appendChild( ext_table_ele )

    subdet_ele = create_element_with_text(doc, 'SUBDET', subdet )
    channel_ele.appendChild( subdet_ele )

    ieta_ele = create_element_with_text(doc, 'IETA', ieta )
    channel_ele.appendChild( ieta_ele )

    iphi_ele = create_element_with_text(doc, 'IPHI', iphi )
    channel_ele.appendChild( iphi_ele )

    # --------------------------
    # END CHANNEL
    # --------------------------
    
    data_set.appendChild( data_element )
    # --------------------------
    # END DATA_SET
    # --------------------------


def MakeStandardDataSetHeader( doc, comment ) :

    # --------------------------
    # BEGIN DATA_SET
    # holds some more header info, then the data
    # --------------------------
    data_set = doc.createElement( 'DATA_SET' )
    
    # add comment description
    commentdesc = create_element_with_text(doc, 'COMMENT_DESCRIPTION', comment )
    data_set.appendChild( commentdesc )
    
    # add timestamp
    timestamp = create_element_with_text(doc, 'CREATE_TIMESTAMP', get_timestamp() )
    data_set.appendChild( timestamp )
    
    #add user
    user = create_element_with_text(doc, 'CREATED_BY_USER', get_user() )
    data_set.appendChild( user )
    
    # add version -- unclear if the format is important
    version = create_element_with_text(doc, 'VERSION', comment  )
    data_set.appendChild( version ) 

    return data_set


def WriteStandardOutput( doc, output_file ) :

    # --------------------------
    # Write the xml
    # Do some manual formatting
    # such that the fields with
    # just a text node are on
    # the same line
    # Simpler code is commented
    # out below
    # --------------------------
    basicXml = doc.toprettyxml(indent='  ')
    text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
    finalXml = text_re.sub('>\g<1></', basicXml)
    #print finalXml

    if not output_file.count('.xml') :
        output_file = output_file + '_%s.xml'

    outfile = open( output_file, 'w' )
    outfile.write(finalXml)
    outfile.close()

    os.system( 'zip %s.zip %s' %( output_file, output_file) )

def ReadFile( fname, det_column='det' ) :

    data = DBData()

    # open the input file
    file = open( fname, 'r' ) 

    if not file :
        print 'Failed to open file ', fname
        return data

    headers = []
    entries = []
    # grab the column labels on the first line
    read_non_channel_data = False
    header_data = {}
    additional_entry_number = 0
    for line in file :

        headers = line.split()

        if read_non_channel_data :

            if headers.count( '#' ) :
                read_non_channel_data = False
            else :
                print 'read non header data'
                if len( headers ) == 1 : 
                    header_data.setdefault( 'info', []).append( headers[0] )
                if len( headers ) == 2 : 
                    header_data[headers[0]] = headers[1]
                else :
                    header_data[ tuple( headers[:-1] ) ] = headers[-1]

        # find the pound at the
        # beginning of the line and remove it
        pound_ent = None
        for ent in headers :
            if ent.count('#') :
                pound_ent = ent
        if pound_ent is not None :
            headers.remove( pound_ent )

            if 'Non-channel' in headers and 'data' in headers :
                read_non_channel_data = True
            else :
                data.set_headers( headers )

        elif not read_non_channel_data :
            entries = line.split()
            if len( entries ) > len( data.headers ) :
                print 'WARNING -- Parsed %d columns, but expected %d from the headers' %( len( entries ), len( data.headers ) )
                print 'Expanding to %d additional header ' %( len(entries) - len( data.headers ) )
                for i in range( 0, len(entries) - len( data.headers ) ) :
                    additional_entry_number += 1
                    data.headers.append( 'addtl%d' %additional_entry_number )

            data.add_entry( entries )

    data.set_header_data( header_data )

    split_data = {}

    HCALDets = ['HB', 'HE', 'HO', 'HF', 'HOX']
    ZDCDets = ['ZDC_EM', 'ZDC_HAD', 'ZDC_LUM']
    CALIBDets = ['CALIB_HE', 'CALIB_HB', 'CALIB_HO', 'CALIB_HF']
    HTDets = ['HT']

    det_column = data.headers.index( det_column )
    for entry in data.entries :

        entry_det = entry[det_column]

        if entry_det in HCALDets :
            add_split_entry( 'HCAL', split_data, entry, data.headers, data.header_data )
        if entry_det in ZDCDets :
            add_split_entry( 'ZDC', split_data, entry, data.headers, data.header_data )
        if entry_det in CALIBDets :
            add_split_entry( 'CALIB', split_data, entry, data.headers, data.header_data )
        if entry_det in HTDets :
            add_split_entry( 'HT', split_data, entry, data.headers, data.header_data )


    return split_data

def add_split_entry( name, data_dic, entry, headers, header_data ) :

    if name not in data_dic :
        data_dic[name] = DBData()
        data_dic[name].headers = headers
        data_dic[name].header_data = header_data

        if name == 'ZDC' :
            data_dic[name].detector_name = 'ZDC'
            data_dic[name].channelmap = 'HCAL_ZDC_CHANNELS'
        elif name == 'CALIB' :
            data_dic[name].detector_name = 'HCAL'
            data_dic[name].channelmap = 'HCAL_CALIB_CHANNELS'
        elif name == 'HT' :
            data_dic[name].detector_name = 'HCAL'
            data_dic[name].channelmap = 'HCAL_TRIG_TOWER_CHANNELS'
        else :
            data_dic[name].detector_name = 'HCAL'
            data_dic[name].channelmap = 'HCAL_CHANNELS'


    data_dic[name].add_entry( entry )


def check_input_compatibility( file_data, required_columns, input_file ) :

    if not set( file_data.get_headers() ).issubset( set( required_columns ) ) :
        print 'Did not get all input columns needed for %s.  Check the input file!' %input_file
        print 'file_data : '
        print file_data.get_headers()
        print 'epxected : '
        print required_columns
        return False

    return True

def create_element_with_text( doc, elename, text ) :

    if not isinstance( text, str ) :
        text = str(text)

    ele = doc.createElement( elename )
    text = doc.createTextNode( text )
    ele.appendChild( text )

    return ele

def create_element_with_attrs( doc, name, attrs={} ) :

    ele = doc.createElement( name )
    for key, val in attrs.iteritems() :
        ele.setAttribute( key, val )

    return ele


def get_timestamp(  ) :
    # time must be in this format for successful
    # database upload
    timestr = time.strftime( '%Y-%m-%d %H:%M:%S.0' )
    return timestr

def get_user() :
    return getpass.getuser()
    




class DBData :

    def __init__(self) :
        self.headers = []
        self.entries = []
        self.header_data = {}

    def set_headers( self, headers ) :
        self.headers = headers

    def set_header_data( self, header_data ) :
        self.header_data = header_data

    def get_headers( self ) :
        return self.headers

    def add_entry( self, data ) :
        if len(data) != len(self.headers) :
            print 'Did not get the correct number of entries!'
            return
        else :
            self.entries.append( data )

    def loop_entries( self ) :
        for entry in self.entries :
            yield dict( zip( self.headers, entry ) )

if __name__ == '__main__' :
    main()
