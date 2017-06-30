from argparse import ArgumentParser
import sys
import os
import math
import subprocess
import re
import uuid
import getpass
import time
import random
from glob import glob, iglob

#-----------------------------------------------------------------------------------------------------        
#                               submit_jobs_penn.py
#
# Author  : Josh Kunkle
# Contact : jkunkle@cern.ch
# SVN     : svn+ssh://svn.cern.ch/reps/penn/PennBatch/trunk/
# Readme  : svn+ssh://svn.cern.ch/reps/penn/PennBatch/trunk/README
#
# Major Revisions :
#
#   2011-08-04 - Module creation
#   2013-07-15 - Some cleanup
#
#-----------------------------------------------------------------------------------------------------        

#-----------------------------------------------------------------------------------------------------        
def ParseOptions() :

    parser = ArgumentParser(usage='python submit_jobs_penn.py --dataset dirname[,dirname2, ...] ' \
            '--output ouputdir [--nFilesPerJob ##] [--nJobs ##] ' )

    #---------------------------------------
    # Required arguments
    #---------------------------------------
    
    parser.add_argument('--dataset', dest='dataset', default=None, required=True,
            help='Path to dataset or comma separated list of paths to datasets' )
    
    parser.add_argument('--output', dest='output', default=None, required=True,
            help='Location of output (only userdisk is supported'                    )
    
    parser.add_argument('--script', dest='script', default=None, required=True,
            help='Full path to script to run'                                         )
    
    #---------------------------------------
    # Commonly used arguments
    #---------------------------------------

    parser.add_argument('--submit', action='store_true', dest='submit',
            default=False, help='Submit jobs'                                           )

    parser.add_argument('--nFilesPerJob', dest='nFilesPerJob', type=int, default=0,
            help='Number of files to run in each job',          )
    
    parser.add_argument('--nJobs', dest='nJobs', type=int, default=0,
            help='Number of jobs to run' )

    parser.add_argument('--module-args', dest='module_args', default='',
            help='Arguments that are passed to the script to be run on the batch node' )

    parser.add_argument('--key', dest='key', default=None, 
            help='Specify key to match in dataset name. Also can be a comma separated list of keys' )

    parser.add_argument('--overwrite', dest='overwrite', default=False, action='store_true',
            help='Overwrite output directory'                                         )
    
    parser.add_argument('--xrootd-mirror', dest='xrootd_mirror', default=None,
            help='Location on local disk which mirrors the xrootd directory' )
    
    #---------------------------------------
    # Other and specialized arguments 
    #---------------------------------------

    parser.add_argument('--exec-file', dest='exec_file', default=None,
            help='Do not submit, but write submit command to provided file'                                         )

    parser.add_argument('--filelist-name',  dest='filelist_name', default=None,
                        help=('Provide input file list as a text file.  Use --input_command to provide the name '
                         'of the file to the script if necessary'))

    parser.add_argument('--filelist-sep',  dest='filelist_sep', default='\n',
                        help='Provide separator for filelist file, default is newline')
    
    parser.add_argument('--priority', dest='priority', default=0 , type=int,
                        help='Set job priority (relative to jobs by the same user)'                                           )
    
    parser.add_argument('--transfer-input-files' ,dest='transfer_input_files', default=False, action='store_true',
                       help=('transfer input files to the local machine where the job runs. '
                             'Use this to avoid over taxing the resource where the datasets exist')

    parser.add_argument('--input-format-module', dest='input_format_module', default=None, 
                         help=('name of module that formats the input files to the job.  It should '
                               'return a list of file input arguments to be supplied to the script'))

    parser.add_argument('--additional-input-path', dest='additional_input_path', default=None, 
                         help=('command and path to additional input for the job keyed by the job number.  Should '
                               'contain an string formatting operator to supply the job directory' ))

    parser.add_argument('--input-command', dest='input_command', default='--files', 
                        help=('option supplied to the script that will be run on the batch nodes '
                              'to pass a list of input files.  '
                              'use an empty string to give arguments with no flag '))
    
    parser.add_argument('--newExecutableName', dest='newExecutableName', default=None, 
                        help=('Change the name of the executable.  This has no practical '
                              'purpose except to change the executable name that is shown '
                              'when you call condor_q'
                             ))
    
    options = parser.parse_args()

    return options

#-----------------------------------------------------------------------------------------------------        
#-----------------------------------------------------------------------------------------------------        
def main(options) :

    print 'Input options : '
    print vars(options)
    run_job_submission(**vars(options))

# Each argument to this function is an option to the script.  See
# matching option entries above for information
#-----------------------------------------------------------------------------------------------------         
def run_job_submission(**kwargs) :

    # Required inputs
    dataset         = kwargs.get('dataset', None) 
    output          = kwargs.get('output', None) 
    xrootd_mirror   = kwargs.get('xrootd_mirror', None) 
    script          = kwargs.get('script', None) 
    starting_job_id = kwargs.get('starting_job_id', 0)
    submit          = kwargs.get('submit', False)
    overwrite       = kwargs.get('overwrite', False)

    if script is None :
        print 'A script is required'
        sys.exit(-1)

    if output is None :
        print 'An output location is required'
        sys.exit(-1)

    if dataset is None :
        print 'A dataset is required'
        sys.exit(-1)

    datasets = []
    if dataset is not None :
        datasets = dataset.split(',')

    #
    # This functionality is intended to check that the arguments
    # passed by --module-args are compatible with the script 
    # options.  Maybe try to resurrect it sometime 
    #

    #testarea = os.getenv('TestArea')
    #if not check_module_args('%s/PhysicsNtuple/PhysicsAlgs/macros/%s' %(testarea, options.script), options.module_args) :
    #    print 'Checking module arguments failed!  This will cause the jobs to fail.  Please Check!'
    #    sys.exit(-1)

    if datasets is None :
        formatted_file_list = { 0: '' }
    else :
        job_file_list, formatted_file_list = SplitIntoJobs(datasets, kwargs)
        
    if not job_file_list :
        print 'Could not parse dataset contentes into a file list'

    if submit :    

        #check if output diretory exists
        #Overwrite only if the user requests to do so
        #************************
        # make the parent directory on the srm
        # the jobs with make their own job directory
        # this will improve submit time
        if output.count('/xrootd') :
            os.system('xrd hn.at3f mkdir %s' %(output[len('/xrootd'):]))
        else :
            os.system('mkdir %s' %output)

        for job_index, job_files in job_file_list.iteritems() :
            make_output_dir(output, job_index+starting_job_id, overwrite)
            # Make mirror direcotry
            if xrootd_mirror is not None :
                make_output_dir(xrootd_mirror, job_index+starting_job_id, overwrite)

        submitargs = dict(kwargs)
        submitargs['job_file_list'] = job_file_list
        submitargs['formatted_file_list'] = formatted_file_list
        return SubmitJobsPenn(submitargs) 

    return 0, 1
      
        
#-----------------------------------------------------------------------------------------------------         
def SplitIntoJobs(in_path, kwargs ) :
    
    # input options
    in_nFilesPerJob     = kwargs.get('nFilesPerJob', 0) 
    in_nJobs            = kwargs.get('nJobs', 0)
    filekey             = kwargs.get('key', None)
    input_format_module = kwargs.get('input_format_module', None)

    Formatter = None
    if input_format_module is not None :
        Formatter = __import__(input_format_module)

    job_file_list = {}
    fkeys = [None]
    if filekey is not None :
        fkeys = filekey.split(',')

    # by default get the files from srm.  Otherwise, use the
    # formatter provided on the command line
    arg_files = []
    print 'getting files'
    if Formatter is not None :
        arg_files = Formatter.format_files(in_path, fkeys)
    else :
        for in_pathone in in_path:
            if 'DS' in in_pathone:
                arg_files += get_files_from_dq2(in_pathone, fkeys)
            else:
                arg_files += get_files_from_srm(in_pathone, fkeys)

    if len(arg_files) == 0 :
        print 'WARNING - No Argument files return from formatter!'

    # randomize the argument files so that individual jobs get an evenly distributed set of files
    arg_files = random.sample(arg_files, len(arg_files))

    # depending on what the user input, calculate the number of jobs and/or files per job
    
    #NJobs provided,  calculate nFilesPerJob
    if in_nFilesPerJob == 0 and in_nJobs > 0 :
        nJobs = in_nJobs
        nFilesPerJob = int(math.ceil(float(len(arg_files))/in_nJobs))
        if nFilesPerJob == 0 :
            nFilesPerJob = 1
    
    elif in_nJobs == 0 and in_nFilesPerJob > 0 :
        nJobs = int(math.ceil(float(len(arg_files))/in_nFilesPerJob))
        nFilesPerJob = in_nFilesPerJob
    
    #nFilesPerJob provided, calculate nJobs
    elif in_nFilesPerJob == 0 and in_nJobs == 0 :
        print 'Please provide nFilesPerJob or NJobs or both'
        nFilesPerJob = 1
        nJobs = 1

    else :
        nFilesPerJob = 1
        nJobs = 1
    
    #make a dictionary that associates a job id to a list of files

    for fkey in fkeys :
        fcounter = 0
        jcounter = 0

        # get all files matching the key
        if fkey is None :
            selected_files = arg_files
        else :
            selected_files = filter(lambda x: x.find(fkey) != -1, arg_files)

        # split into sub-lists based on the number of jobs.  last job may have fewer files
        split_files = [selected_files[i:i+nFilesPerJob] for i in range(0, len(selected_files), nFilesPerJob)]

        # The splitting can fail to give the correct number of jobs 
        # we'll get fewer jobs than we expected.  The next bit of code
        # aims to fix this
        if len(split_files) != nJobs and in_nJobs == 0 :
            print 'WARNING - Did not split files correctly...fixing the problem...'
            print 'njobs = %d' %nJobs
            print 'split = %d' %len(split_files)
            print 'nfiles = %d' %len(selected_files)
            print 'nfilesperjob = %d' %nFilesPerJob
            print 'This is the pattern of files that we got'
            for files in split_files :
                print [ 'x' for file in files ]

            n_iter = 0
            iter_max = abs( nJobs - len(split_files)) + 10 
            while len(split_files) != nJobs :
                    
                # if we've gotten to 1 file per job, go ahead and submit
                max_files_per_split = max( [ len(fs) for fs in split_files ] )
                if max_files_per_split == 1 :
                    print 'Already have 1 file per job!.  Submitting 1 file per job.'
                    break

                n_iter += 1
                new_entry = []

                #get a random list of entries in split_files of size ( nFilesPerJob-1 ) 
                #randomly remove a job from each of these
                randlist = random.sample(xrange(0, len(split_files) ), nFilesPerJob-1)
                for i in randlist :
                    # only remove if there are some available
                    if len(split_files[i]) > 1 :
                        new_entry.append(split_files[i].pop(0))
                split_files.append(new_entry)

                # bail if this isn't working
                if n_iter > iter_max:
                    print 'ERROR - Did not split files correctly'
                    print 'njobs = %d' %nJobs
                    print 'split = %d' %len(split_files)
                    print 'nfiles = %d' %len(selected_files)
                    print 'nfilesperjob = %d' %nFilesPerJob
                    sys.exit(-1)

            print 'Repaired problem.  this is the new pattern of files'
            for files in split_files :
                print [ 'x' for file in files ]

        if len(split_files) != nJobs and in_nJobs == 0  :
            print 'ERROR - Did not split files correctly'

        # if user has input nJobs, use that
        if in_nJobs != 0 :
            if nJobs < len(split_files) :
                split_files = split_files[0:nJobs]
            

        for jcounter, sub_list in enumerate(split_files) :
            job_file_list[jcounter] = sub_list
        
        formatted_list = None
        if Formatter is not None :

            formatted_list = {}
            for key, entry in job_file_list.iteritems() :
                formatted_list[key] = Formatter.format_job_files(entry, fkey)

        else :
            #default behavior
            formatted_list = {}
            for key, entry in job_file_list.iteritems() :
                formatted_list[key] = ','.join(entry)
        
    return job_file_list, formatted_list

#-----------------------------------------------------------------------------------
def SubmitJobsPenn(kwargs) :

    #input arguments
    job_file_list = kwargs.get('job_file_list', {}) 
    output        = kwargs.get('output', '')
    exec_file     = kwargs.get('exec_file', None)

    cluster = -1

    # create job description that will
    # reside in the mirror directory
    print 'create job desc file'
    transfer_output_files=False
    if output.count('/xrootd') :
        transfer_output_files=True

    jdargs = dict(kwargs)
    jdargs['transfer_output_files'] = transfer_output_files
    # create the job description file
    desc_file = create_job_desc_file(jdargs)

    print 'submit to condor'
    condor_file = desc_file

    # do not submit jobs, instead write to
    # the provided file
    if exec_file is not None :
        print 'Writing submit command to %s' %exec_file
        file = open(exec_file, 'a')
        file.write('condor_submit %s\n' %condor_file)
        file.close()

        return ( -1, len(job_file_list) )
    else :

        print 'condor_submit %s' %condor_file
        res = subprocess.Popen(['condor_submit', condor_file], stdout=subprocess.PIPE).communicate()[0]

        submit_res = res.split('\n')
        for line in submit_res :
            res = re.match('\d+ job\(s\) submitted to cluster (\d+)\.', line) 
            if res is not None :
                print line
                cluster = res.group(1)

        return (cluster, len(job_file_list) )


#-----------------------------------------------------------------------------------
def create_job_desc_file(kwargs) :

    # input options
    job_file_list         = kwargs.get('job_file_list')
    formatted_file_list   = kwargs.get('formatted_file_list')
    output                = kwargs.get('output')
    xrootd_mirror         = kwargs.get('xrootd_mirror', None)
    script                = kwargs.get('script')
    module_args           = kwargs.get('module_args', '')
    input_command         = kwargs.get('input_command')
    additional_input_path = kwargs.get('additional_input_path', None)
    transfer_input_files  = kwargs.get('transfer_input_files', None)
    transfer_output_files = kwargs.get('transfer_output_files', False)
    priority              = kwargs.get('priority', 0)
    starting_job_id       = kwargs.get('starting_job_id', 0)
    filelist_name         = kwargs.get('filelist_name', None)
    filelist_sep          = kwargs.get('filelist_sep', '\n')

    # The user has requested to transfer the input files
    # If the input files are on the xrootd space, we have to create
    # a script that copies them manually and use that later
    orig_script = script
    files_output = output
    if xrootd_mirror is not None :
        files_output = xrootd_mirror

    orig_script_name = os.path.basename(orig_script)
    
    newname = make_transfer_script( files_output, orig_script_name, kwargs )
    script = files_output+'/' + newname

    if transfer_input_files :
        #Generate or get file transfer queue
        #Generate in 10 minute intervals
        curr_gmtime = time.gmtime()
        curr_min = (int(curr_gmtime[4])/10)*10
        queue_name = time.strftime('%Y_%m_%d_%H',curr_gmtime)
        queue_name += '_%d' %curr_min
        user = getpass.getuser()
        file_queue_dir = '/disk/userdata00/atlas_data2/%s/condor_interface_queues/%s' %(user,queue_name)
        if not os.path.isdir( file_queue_dir ) :
            os.makedirs( file_queue_dir )
            os.system('touch %s/queue.txt' %file_queue_dir )



    # the header of the job description file
    desc_entries = [
                    '#Use only the vanilla universe',
                    'universe = vanilla',
                    '# This is the executable to run.  If a script,',
                    '#   be sure to mark it "#!<path to interp>" on the first line.',
                    'Executable = %s' %script,
                    '# Filename for stdout, otherwise it is lost',
                    'output = stdout.txt',
                    'error = stderr.txt',
                    '# Copy the submittor environment variables.  Usually required.',
                    'getenv = True',
                    '# Copy output files when done.  REQUIRED to run in a protected directory',
                    'when_to_transfer_output = ON_EXIT_OR_EVICT',
                    'priority=%d' %priority
                    ]

    
    if xrootd_mirror is None :
        desc_entries += [ 'should_transfer_files = YES' ]

    for job_index, files_arg in formatted_file_list.iteritems() :

        outid = 'Job_%04d' %(job_index+starting_job_id)
        initialdir = '%s/%s' %(files_output, outid)

        job_module_args = module_args

        desc_entries += [
                         'Initialdir = %s' %initialdir,
                         '# This is the argument line to the Executable'
                        ]
        # assemble the argument command

        arg_command = ['arguments = "',
                       '--script %s' %orig_script,
                       '--files %s' %files_arg,
                       '--input-command \' %s \'' %input_command,
                       '--module-args \' %s \'' %job_module_args,
                      ]

        # if transferring files, pass the 
        # queue to the job.  otherwise tell the script to 
        # not transfer files
        if transfer_input_files :
            arg_command += ['--file-queue-dir %s' %file_queue_dir ]
        else :
            arg_command += [ '--no-transfer-input' ]

        # if transferring output files, pass the output
        if transfer_output_files :
            new_output = output+'/Job_%04d' %(job_index+starting_job_id)
            arg_command += [ '--output %s '%new_output ]

        if additional_input_path is not None :
            arg_command += [ ' --additional-input %s' %(additional_input_path % outid) ]

        if filelist_name is not None :
            arg_command += [ ' --filelist-name %s --filelist-sep %s ' %( filelist_name, filelist_sep )]

        # End of arguments.  Add additional arguments above
        arg_command += ['"']

        desc_entries +=  [ ' '.join(arg_command) ]

        desc_entries += [
                          '# Queue job',
                          'queue'
                        ]

    #Determine the job description file name
    desc_name = 'job_desc.txt'

    desc_file_name = files_output+'/'+desc_name

    descf = open(desc_file_name, 'w')

    descf.write('\n'.join(desc_entries))
    descf.close()

    print 'cp %s %s' %(desc_file_name, output) 
    os.system('cp %s %s' %(desc_file_name, output) )

    return desc_file_name

#-----------------------------------------------------------------------------------
def make_transfer_script(output, script, kwargs) :

    script_loc = os.path.realpath(__file__)

    script_dir = os.path.dirname(script_loc)

    if not os.path.isfile(script_dir +'/condor_interface.py') :
        print 'ERROR'
        print 'Could not find "condor_interface.py".  This is required to run jobs on the batch.'
        print 'Most likely this is because submit_jobs_penn.py was checked out or run outside of PennBatch.'
        print 'To fix this problem, check out all of PennBatch and run submit_jobs_penn.py from within PennBatch'
        sys.exit(-1)

    executable_name = kwargs.get('newExecutableName', None)
    if executable_name is None :
        executable_name = '.'+script
    print 'cp %s/condor_interface.py %s/%s' %(script_dir, output, executable_name)
    os.system('cp %s/condor_interface.py %s/%s' %(script_dir, output, executable_name))
    return executable_name

#-----------------------------------------------------------------------------------
#def check_module_args(script, args) :
#    #
#    # This function is intended to check that the arguments
#    # passed by --module-args are compatible with the script 
#    # options.  Maybe try to resurrect it sometime 
#    #
#
#    #try :
#    #    subprocess.check_call(['python', script] +  args.split() + ['-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    #except subprocess.CalledProcessError :
#    #    return False
#    subprocess.check_call(['python', script] +  args.split() + ['-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#
#    return True

#-----------------------------------------------------------------------------------
def expand_paths(in_path) :

    if not isinstance(in_path, list) :
        in_path = [in_path]

    paths = []
    for each_path in in_path :

        if os.path.isdir(each_path) :
            paths.append(each_path)
        else :
            parent_dir = '/'.join(each_path.split('/')[0:-1])
            ds_name = each_path.split('/')[-1]
            for entry in os.listdir(parent_dir) :
                if entry.find(ds_name) != -1 :
                    paths.append(parent_dir+'/'+entry)


    return paths
#---------------------------------------------------------
def get_files_from_dq2(paths, key) :

    if not isinstance(paths, list) :
        paths = [paths]
        
    matched_files = []
        
    for each_path in paths :

        print 'searching dq2 for %s' %each_path.lstrip('DS')

        worker_path = 'root://hn.at3f'

        dq2cmd = "dq2-ls " + "-fpL " + "UPENN_LOCALGROUPDISK " + each_path.lstrip('DS')

        dq2process = subprocess.Popen(dq2cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out,err = dq2process.communicate()

        dq2lines = out.split('\n')

        
        for dq2line in dq2lines:
            if dq2line.find('root') != -1:
                if dq2line.find('srm:') != -1:
                    matched_files.append(dq2line.replace('srm://srm.hep.upenn.edu:8443/srm/v2/server?SFN=/disk/space00/','root://hn.at3f//'))


    matched_files = list(set(matched_files))

    return matched_files
                                                                                                                    

#-----------------------------------------------------------------------------------
def get_files_from_srm(paths, key) :

    if not isinstance(paths, list) :
        paths = [paths]

    real_paths = [os.path.realpath(p) for p in paths]

    matched_files = []

    for each_path in real_paths :

        print 'searching srm for %s' %each_path

        #convert to worker path
        #worker_path = 'root://hn.at3f//' + '/'.join(each_path.split('/')[2:])
        worker_path = 'root://hn.at3f'
        modpath = each_path
        res = re.match('/xrootd(.*)', each_path) 
        if res is not None :
            modpath = res.group(1)


        for top, dirs, files, sizes in walk_xrootd(modpath) :
            for file in files :
                if file.find('root') != -1 :

                    if key is not None :
                        match = False
                        for k in key :
                            if k is None or file.find(k) != -1:
                                match = True
                                break
                        if match :
                            #matched_files.append(worker_path+'//'+top.lstrip('/')+'/'+file)
                            matched_files.append(worker_path+'//'+top.lstrip('/')+'/'+os.path.split(file)[1])
                    else :
                        #matched_files.append(worker_path+'//'+top.lstrip('/')+'/'+file)
                        matched_files.append(worker_path+'//'+top.lstrip('/')+'/'+os.path.split(file)[1])

    matched_files = list(set(matched_files))
    return matched_files

#---------------------------------------------------------
def parse_xrd_dir(path, DEBUG=False) :

    # remove leading xrootd for using xrd dirlist
    #res = re.match('/xrootd/(.*)', path)
    #if res is not None :
    #    path = res.group(1)

    directories = []
    sizes = []
    files = [] 

    #print "xrd hn.at3f dirlist "+path
    #lines = os.popen("xrd hn.at3f dirlist "+path).readlines()
    #output = str("").join(lines)

    # glob bitches
    print '/xrootd'+path+'/*'
    for entry in iglob('/xrootd'+path+'/*') :
        if os.path.isdir(entry)  :
            directories.append(entry.split('/')[-1])
        if os.path.isfile(entry) :
            files.append(entry.split('/')[-1])
    
    
    return (directories, files, [0]*len(files))
    
    output_lines = output.rstrip('\n').split('\n')

    if len(output_lines) == 0 :
        return directories, files, sizes
    for line in output_lines :

        if len(line) == 0:
            return directories, files, sizes

        if DEBUG :
            print "Line is"
            print line


        try :
            obj = line.split()[4].split('/')[-1]
        except Exception,e :
            print e
            print "Error in parsing output"
            sys.exit(-1)

        if DEBUG:
            print "obj is:"
            print obj

        if line[0] == 'd' :
            directories.append(obj)
        elif line[0] == '-' or line[0] == 'm':
            files.append(obj)
            sizes.append(int(line.split()[1]))
        else :
            print 'could not determine if object is a file or directory for'
            print line
            

    return directories, files, sizes

#---------------------------------------------------------
def walk_xrootd(path) :

    dirs, files, sizes = parse_xrd_dir(path)
    yield path, dirs, files, sizes
    if len(dirs) > 0 :
        for dir in dirs :
            for new_path, new_dirs, new_files, new_sizes in walk_xrootd('%s/%s' %(path, dir)) :
                yield new_path, new_dirs, new_files, new_sizes


#-----------------------------------------------------------------------------------
def make_output_dir(output, job_index, overwrite) :

    try :
        #if output.find('xrootd') != -1 :
        #    print ('xrd hn.at3f mkdir %s/Job_%04d' %(output[len('/xrootd'):], job_index))
        #    os.system('xrd hn.at3f mkdir %s/Job_%04d' %(output[len('/xrootd'):], job_index))
        #else :
        #    os.makedirs('%s/Job_%04d' %(output, job_index))
        if output.find('xrootd') == -1 :
            print ('%s/Job_%04d' %(output, job_index))
            os.makedirs('%s/Job_%04d' %(output, job_index))
    except OSError :
        if overwrite :
            print 'Will overwrite output directory'
            if output.find('xrootd') != -1 :
                os.system('xrd hn.at3f rmdir %s' %(output[len('/xrootd'):]))
            else :
                os.system('rm -rf %s' %output)

            if output.find('xrootd') != -1 :
                os.system('xrd hn.at3f mkdir %s/Job_%04d' %(output[len('/xrootd'):], job_index))
            else :
                os.makedirs('%s/Job_%04d' %(output, job_index))
        else :
            print 'Output directory already exists.  Add --overwrite to over-write the output directory'
            sys.exit(0)

class FileCacheSvc :

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def _LoadCache(self, openstate='r') :

        self.cache = {}

        curr_loc = os.path.dirname(os.path.realpath(__file__))
        if os.path.isfile(curr_loc+'/'+ _cache_file) :
            cachefile = open(curr_loc+'/'+ _cache_file, 'r' )
            try :
                self.cache = pickle.load(cachefile)
                cachefile.close()
            except EOFError :
                pass

    def _WriteCache(self, openstate='r') :

        curr_loc = os.path.dirname(os.path.realpath(__file__))
        cachefile = open(curr_loc+'/'+ _cache_file, 'w')
        pickle.dump(self.cache, cachefile)
        cachefile.close()


    def GetCachedFiles(self, formatter, dirs) :

        #check if file is loaded
        if not getattr(self, 'reading_cache', False ) :
            self._LoadCache('r')

        match_formatter = self.cache.get(formatter, [])
        if match_formatter :
            for dirlist, filelist in match_formatter :

                #match the dirlist and return the files
                cache_dirs = set(dirlist)
                input_dirs = set(dirs)

                if len( cache_dirs - input_dirs ) == 0 :
                    return filelist

        return []

    def StoreFiles(self, formatter, dirs, files) :

        #check if file is loaded
        if not getattr(self, 'reading_cache', False ) :
            self._LoadCache('w')

        self.cache.setdefault( formatter, [] )

        #don't check, just put it in
        self.cache[formatter].append((dirs, files))

        self._WriteCache()


if __name__ == '__main__' :
    main(ParseOptions())
