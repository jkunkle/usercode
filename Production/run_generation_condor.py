from argparse import ArgumentParser
import os
from uuid import uuid4
import subprocess

parser = ArgumentParser( )

parser.add_argument('--prod_dir', dest='prod_dir', required=True, help='path to processing directory' )
parser.add_argument('--gridpack', dest='gridpack', required=True, help='path to gridpack' )
parser.add_argument('--nevt', dest='nevt', type=int, default=20000, help='number of events to run.  Each job will contain 1000 events' )
parser.add_argument('--nevtPerJob', dest='nevtPerJob', type=int, default=1000, help='number of events to run per job default = 1000' )

options = parser.parse_args()


def main() :

    if not os.path.isfile( options.gridpack ) :
        print 'Gridpack does not exist! Exiting!'
        return


    # no longer need certificate
    #print 'FIRST MAKE A GRID CERTIFICATE'
    #os.system( 'voms-proxy-init -voms cms -rfc ' )


    if not os.path.isdir( options.prod_dir ) :
        os.makedirs ( options.prod_dir )

    nJobs = options.nevt / options.nevtPerJob

    print 'Will run %d jobs' %nJobs

    output_name = options.prod_dir.rstrip('/').split('/')[-1]

    job_desc_text = []

    result = subprocess.Popen( ['voms-proxy-info'], stdout=subprocess.PIPE ).communicate()[0]

    proxy_path = None
    for line in result.split('\n') :
        splitline = line.split(':')
        if splitline[0].count('path') :
            proxy_path = splitline[1]
            break
            
    job_desc_text.append( '#Use only the vanilla universe' )
    job_desc_text.append( 'universe = vanilla' )
    job_desc_text.append( '# This is the executable to run.  If a script,') 
    job_desc_text.append( '#   be sure to mark it "#!<path to interp>" on the first line.' ) 
    job_desc_text.append( '# Filename for stdout, otherwise it is lost' ) 
    job_desc_text.append( 'output = stdout.txt' ) 
    job_desc_text.append( 'error = stderr.txt' ) 
    job_desc_text.append( '# Copy the submittor environment variables.  Usually required.' ) 
    job_desc_text.append( 'getenv = True' ) 
    job_desc_text.append( '# Copy output files when done.  REQUIRED to run in a protected directory' ) 
    job_desc_text.append( 'when_to_transfer_output = ON_EXIT_OR_EVICT' ) 
    job_desc_text.append( 'should_transfer_files = YES' ) 
    # no longer need certificate
    #job_desc_text.append( 'transfer_input_files = %s' %proxy_path ) 
    job_desc_text.append( 'priority=0' ) 

    for job in range( 0, nJobs) :

        job_dir = 'Job_%04d' %( job )
        scriptName = 'r%04d.sh' %( job )

        if not os.path.isdir( '%s/%s' %( options.prod_dir, job_dir ) ) :
            os.makedirs( '%s/%s' %( options.prod_dir, job_dir ) ) 

        os.system( 'python /home/jkunkle/Programs/run_all_generation_steps.py  --prod_dir %s/%s --name %s --gridpack %s  --nevt %d --writeShellScript --scriptName %s ' %( options.prod_dir, job_dir, output_name, options.gridpack, options.nevtPerJob, scriptName) )

        #job_desc_text.append( 'Executable = /home/jkunkle/Programs/run_all_generation_steps.py' )
        job_desc_text.append( 'Executable = %s/%s/%s'%( options.prod_dir, job_dir, scriptName ) )
        job_desc_text.append( 'Initialdir = %s/%s'  %(options.prod_dir, job_dir) )
        job_desc_text.append( '# This is the argument line to the Executable' )
        #job_desc_text.append( 'arguments = " --prod_dir %s/%s --name %s --gridpack %s --nevt %d" ' %( options.prod_dir, job_dir, output_name, options.gridpack, options.nevtPerJob ) )
        job_desc_text.append( '# Queue job' )
        job_desc_text.append( 'queue' )


    job_desc_file_name = '%s/job_desc.txt' %( options.prod_dir )

    job_desc_file = open( job_desc_file_name, 'w' )

    for line in job_desc_text :
        job_desc_file.write( '%s \n' %line )


    job_desc_file.close()

    os.system( 'condor_submit %s ' %( job_desc_file_name ) )




main()
