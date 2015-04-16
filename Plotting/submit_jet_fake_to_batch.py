import os
output = '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/WggPlots_2015_04_13'
#channels = ['mu', 'elzcr', 'elfull', 'elzcrinvpixsubl', 'elzcrinvpixlead', 'elfullinvpixsubl', 'elfullinvpixlead']
channels = ['mu', 'elfull', 'elfullinvpixsubl', 'elfullinvpixlead']
#jetfitvars = ['sigmaIEIE', 'chIsoCorr', 'phoIsoCorr']
jetfitvars = ['phoIsoCorr']
jetffcorrinputs = ['nom', 'veryloose', 'loose', 'tight', 'None']
corr_types = ['nom', 'asymcorr533', 'asymcorr855', 'asymcorr1077', 'asymcorr1299', 'asymcorr151111', 'asymcorr201616']

user_base = '/afs/cern.ch/user/j/jkunkle/usercode'
run_base = '%s/Plotting' %(user_base)
output_base = '%s/JetFakeBatchJobs' %run_base

PTBINS='15,25,40,70,1000000'
SYSTFILE='%s/JetFakeTemplatePlots/systematics.pickle' %output
MODULE='%s/Modules/JetFakeFit.py' %(run_base)
OUTPUTJET='%s/JetFakeResultsSyst' %output


if not os.path.isdir( output_base ) :
    os.makedirs( output_base )

# make the output dirs
# so the jobs dont 
# race to create it
if not os.path.isdir( OUTPUTJET ) :
    os.makedirs( OUTPUTJET)

for ch in channels :
    for var in jetfitvars :
        for ffinput in jetffcorrinputs :

            job_name = 'jet_fake_job_%s_%s_%s' %( ch, var, ffinput)
            wrapper_name = '%s.sh' %( job_name)
            log_name = '%s.log' %( job_name)
            err_name = '%s.err' %( job_name)
                    
            file = open( '%s/%s' %(output_base, wrapper_name), 'w')
            file.write( 'source /afs/cern.ch/user/j/jkunkle/.bashrc \n' )
            file.write( 'export WorkArea=%s/Analysis \n' %( user_base) )
            file.write( 'export PYTHONPATH=$PYTHONPATH:%s/Analysis/TreeFilter/Core/python:%s/Analysis/Util/python \n' %( user_base, user_base) )

            for ct in corr_types :
                command = 'python %s/RunMatrixFit.py --samplesConf %s --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile %s/cross_sections/wgamgam.py  --lumi 19400 --outputDir %s --%s --channel %s --syst_file %s --ptbins %s --fitvar %s --ffcorr %s --quiet ' %(run_base, MODULE, run_base, OUTPUTJET, ct, ch, SYSTFILE, PTBINS, var, ffinput)

                file.write( command + '\n' )

            file.close()

            os.system( 'chmod 777 %s/%s' %( output_base, wrapper_name) )

            os.system( 'bsub -e %s/%s -o %s/%s -q 8nh %s/%s' %( output_base, err_name, output_base, log_name, output_base, wrapper_name ) )

