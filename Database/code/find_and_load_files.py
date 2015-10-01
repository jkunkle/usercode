import os
import re
import time
import xml_converter
from optparse import OptionParser

parser = OptionParser()

parser.add_option( '--moveToLoaded', dest='moveToLoaded', default=False, action='store_true', help='Move files to the Loaded directory' )
parser.add_option('--run', dest='run', default=False, action='store_true', help='Run the xml transformation' )
parser.add_option('--makeCopyCommands', dest='makeCopyCommands', default=False, action='store_true', help='move transferred files to the LoadedOnlineDB area' )
parser.add_option('--runFullChain', dest='runFullChain', default=False, action='store_true', help=('Run all steps in an automatic fashion.  ' 
                                                                                                   'First check twice for existing files to be sure that '
                                                                                                   'no changes are occuring.  '
                                                                                                   'Second, Do the conversion for all files  '
                                                                                                   'Third, scp the files to the dropbox  '
                                                                                                   'Last, copy the files to LoadedOnlineDB' )  )

(options,args) = parser.parse_args()

base_dir =  '/nfshome0/hcaldpg/database/Tables/'

def main() :

    currtime = time.localtime()
    
    date = '%04d_%02d_%02d_%02d-%02d' %( currtime[0], currtime[1], currtime[2], currtime[3], currtime[4] )
    
    output_dir = '/nfshome0/hcaldpg/database/Processing/LoadToDB_%s' %date
    
    not_loaded_files = get_not_loaded_files( base_dir )

    if options.moveToLoaded :

        move_files_to_loaded( not_loaded_files )
        
    elif options.makeCopyCommands :

        print '\n'.join(get_copy_commands( not_loaded_files, output_dir ) )

    elif options.runFullChain :

        lock_name = '/nfshome0/hcaldpg/database/Processing/.in_progress'
        if os.path.isfile( lock_name ) :
            print 'An instance of this script is already running!  Will abort!'
            return
        else :
            os.system( 'echo "True" >> %s ' %lock_name)

        # step 1, check that the inputs are stable
        while True :

            # Sleep for 5 seconds and get the
            # files again to check that 
            # no file copies are in progress
            time.sleep(5)
            not_loaded_files_check = get_not_loaded_files( base_dir )

            # first check that the number of 
            # files found is the same
            all_types_match = True
            typedir_len_dict = {}
            for typedir, files in not_loaded_files.iteritems() :
                typedir_len_dict[typedir] = len( files )

            for typedir, files in not_loaded_files_check.iteritems() :
                if len(files) != typedir_len_dict[typedir] :
                    all_types_match = False

            # if a different number of files was
            # found, get the list of files again and
            # repeat the check
            if not all_types_match :
                print 'Did not match all types'
                not_loaded_files = get_not_loaded_files( base_dir )
            else :

                # check that the size of each file is the same
                size_dict = {} 
                for typedir, files in not_loaded_files.iteritems() :
                    for f, size in files :
                        size_dict[f] = size

                all_files_match = True
                for typedir, files in not_loaded_files_check.iteritems() :
                    for f, size in files :
                        if size != size_dict[f] :
                            all_files_match = False

                # if any sizes were different
                # get the list of files again and
                # repeat the check
                # else we're ready to move on
                if not all_files_match :
                    print 'Did not match all file sizes'
                    not_loaded_files = get_not_loaded_files( base_dir )
                else :
                    break


        # step 2, convert the files
        successful_conversions, failed_files = run_file_conversions( not_loaded_files, output_dir, run=True )
        
        if failed_files :
            print 'Failed to convert : '
            for f in failed_files :
                print f

        #step 3, copy to the uploader
        copy_commands = get_copy_commands( successful_conversions, output_dir ) 

        for cmd in copy_commands :
            os.system( 'echo ' + cmd )
            os.system( cmd )

        # step 4, move to loaded
        move_files_to_loaded( successful_conversions )

        os.system( 'rm %s ' %lock_name)


       
    else :

        run_file_conversions( not_loaded_files, output_dir, options.run )

def move_files_to_loaded( not_loaded_files ) :
        
    for type, files in not_loaded_files.iteritems() :

        for f, size in files :
            
            # replace to move to the loaded directory
            destination = f.replace( 'NotLoadedOnlineDB', 'LoadedOnlineDB' )

            # if the file is in a subdirectory, combine the file name
            # with the subdirectory name

            destination_split = destination.split('/')
            loaded_loc = destination_split.index( 'LoadedOnlineDB' )
            remaining = len(destination_split[loaded_loc:])

            if remaining > 2 :
                destination = '/'.join( destination_split[:loaded_loc+1]) + '/'+ '_'.join( destination_split[loaded_loc-1:] )

            os.system( 'echo mv %s %s' %( f, destination ) )
            os.system( 'mv %s %s' %( f, destination ) )

def get_copy_commands( not_loaded_files, output_dir ) :
    
    copy_list = []
    for typedir in not_loaded_files.keys() :

        dirpath = '%s/%s' %( output_dir, typedir )

        if os.path.isdir( dirpath ) :

            for file in os.listdir( dirpath  ) :

                if file.count( '.xml.zip' ) :
                    #copy_list.append('scp %s/%s/%s dbvalhcal@pcuscms34.cern.ch:conditions/ ' %(output_dir, typedir, file ) )
                    #copy_list.append('scp %s/%s/%s hcaldqm03:/var/spool/xmlloader/hcal/prod/conditions/ ' %(output_dir, typedir, file ) )
                    copy_list.append('cp %s/%s/%s /var/spool/xmlloader/hcal/prod/conditions/ ' %(output_dir, typedir, file ) )

    return copy_list


def run_file_conversions( not_loaded_files, output_dir, run=False ) :


    successful_conversions = {}
    failed_files = []
    convert_count = 0
    for typedir, files in not_loaded_files.iteritems() :

        successful_conversions.setdefault( typedir, [] )
    
        function = None
        if typedir == 'HcalChannelQuality'  :
            function = 'MakeHCALChannelQualityXML' 
    
        if typedir == 'HcalGains' :
            function = 'MakeHCALGainsXML'
    
        if typedir == 'HcalL1TriggerObjects'  :
            function = 'MakeHCALL1TriggerObjectsXML'
    
        if typedir == 'HcalLongRecoParams' :
            function = 'MakeHCALLongRecoParamsXML'
    
        if typedir == 'HcalLUTCorrs'  :
            function = 'MakeHCALLUTCorrsXML' 
    
        if typedir == 'HcalLutMetadata' :
            function = 'MakeHCALLUTMetaDataXML'
    
        if typedir == 'HcalMCParams'  :
            function = 'MakeHCALMCParamsXML' 
            
        if typedir == 'HcalPedestals' :
            function = 'MakeHCALPedestalsXML' 
    
        if typedir == 'HcalPedestalWidths'  :
            function = 'MakeHCALPedestalWidthsXML'
        
        if typedir == 'HcalPFCorrs' :
            function = 'MakeHCALPFCorrsXML' 
    
        # No transformation exists for 
        # HcalQIEData
        #if typedir == 'HcalQIEData' :
        #    function = 'MakeHCALQIEDataXML'
    
        if typedir == 'HcalRecoParams' :
            function = 'MakeHCALRecoParamsXML'
            
        if typedir == 'HcalTimeCorrs' :
            function = 'MakeHCALTimeCorrsXML'
            
        if typedir == 'HcalZSThresholds' :
            function = 'MakeHCALZSThresholdsXML'
            
        if typedir == 'HcalElectronicsMap' :
            function = 'MakeHCALElectronicsMapXML'
    
        if typedir == 'HcalRespCorrs' :
            function = 'MakeHCALRespCorrsXML'
    
        if function is not None :

            for f, size in files :
    
                type_output = '%s/%s' %( output_dir, typedir ) 
    
                if run :
                    if not os.path.isdir( type_output ) :
                        os.makedirs( type_output )

                    result = getattr( xml_converter, function) ( f, type_output )

                    if result :
                        convert_count += 1
                        successful_conversions[typedir].append( (f, size ) )
                    else :
                        failed_files.append( f )

                #command = 'python xml_converter.py --inputFile %s --outputDir %s %s ' %(  f, type_output, function)
    print 'Converted %d files' %convert_count
    return successful_conversions, failed_files

def get_not_loaded_files( base_dir ) :

    not_loaded = {}

    for top, dirs, files in os.walk( base_dir ) :
        if top.count('NotLoadedOnlineDB' ) :
    
            typedir = top.split('/')[5]
            type_files = []

            not_loaded.setdefault( typedir, [] )

            if files :
        
                for f in files :

                    file_path = '%s/%s' %( top, f )

                    size = os.path.getsize( file_path )
    
                    not_loaded[typedir].append( ( file_path, size ) )
                        

    return not_loaded
            

main()
