import os
base_data='/eos/cms/store/group/phys_smp/ggNtuples/data'
base_mc='/eos/cms/store/group/phys_smp/ggNtuples/mc'
base_cmkuo='/eos/cms/store/group/phys_egamma/cmkuo'
base_phA = '/eos/cms/store/user/hebda/2012A'
base_phB = '/eos/cms/store/user/hebda/2012B'
base_phD = '/eos/cms/store/group/phys_higgs/cmshgg/rekovic/ggNtuples/RunD'
base_phD2 = '/eos/cms/store/caf/user/cmkuo'

job_conf = [
          #(base_mc,'job_summer12_DYJetsToLL',400),
          #(base_cmkuo, 'job_summer12_WAA_ISR', 20),
          #(base_cmkuo, 'job_summer12_WH_ZH_125', 10),
          #(base_cmkuo, 'job_summer12_WWW', 10),
          #(base_cmkuo, 'job_summer12_WWZ', 10),
          #(base_cmkuo, 'job_summer12_WW_2l2nu', 20),
          #(base_cmkuo, 'job_summer12_WWg', 10),
          #(base_cmkuo, 'job_summer12_WZZ', 10),
          #(base_cmkuo, 'job_summer12_WZ_2l2q', 20),
          #(base_cmkuo, 'job_summer12_WZ_3lnu', 20),
          #(base_cmkuo, 'job_summer12_Zg', 100),
          #(base_cmkuo, 'job_summer12_Wg', 100),
          #(base_cmkuo, 'job_summer12_Wgg_FSR', 20),
          #(base_cmkuo, 'job_summer12_ZZZ', 10),
          #(base_cmkuo, 'job_summer12_ZZ_2e2mu', 10),
          #(base_cmkuo, 'job_summer12_ZZ_2e2tau', 10),
          #(base_cmkuo, 'job_summer12_ZZ_2l2nu', 10),
          #(base_cmkuo, 'job_summer12_ZZ_2l2q', 10),
          #(base_cmkuo, 'job_summer12_ZZ_2mu2tau', 10),
          #(base_cmkuo, 'job_summer12_ZZ_2q2nu', 10),
          #(base_cmkuo, 'job_summer12_ZZ_4e', 20),
          #(base_cmkuo, 'job_summer12_ZZ_4mu', 10),
          #(base_cmkuo, 'job_summer12_ZZ_4tau', 20),
          #(base_cmkuo, 'job_summer12_Wjets', 400),
          #(base_cmkuo, 'job_summer12_diphoton_box_10to25', 10),
          #(base_cmkuo, 'job_summer12_diphoton_box_250toInf', 10),
          #(base_cmkuo, 'job_summer12_diphoton_box_25to250', 10),
          #(base_cmkuo, 'job_summer12_ggH_125', 10),
          #(base_cmkuo, 'job_summer12_ggZZ_2l2l', 10),
          #(base_cmkuo, 'job_summer12_ggZZ_4l', 10),
          #(base_cmkuo, 'job_summer12_t_s', 10),
          #(base_cmkuo, 'job_summer12_t_t', 10),
          #(base_cmkuo, 'job_summer12_t_tW', 10),
          #(base_cmkuo, 'job_summer12_tbar_s', 20),
          #(base_cmkuo, 'job_summer12_tbar_t', 10),
          #(base_cmkuo, 'job_summer12_tbar_tW', 50),
          #(base_cmkuo, 'job_summer12_ttW', 20),
          #(base_cmkuo, 'job_summer12_ttZ', 10),
          #(base_cmkuo, 'job_summer12_ttg', 50),
          #(base_cmkuo, 'job_summer12_ttinclusive', 10),
          #(base_cmkuo, 'job_summer12_ttjets_1l', 200),
          #(base_cmkuo, 'job_summer12_ttjets_2l', 200),

          #(base_data, 'job_muon_2012a_Jan22rereco', 50),
          #(base_data, 'job_muon_2012b_Jan22rereco', 100),
          #(base_data, 'job_muon_2012c_Jan22rereco', 200),
          #(base_data, 'job_muon_2012d_Jan22rereco', 200),
          #(base_data, 'job_electron_2012a_Jan22rereco', 100),
          #(base_data, 'job_electron_2012b_Jan22rereco', 200),
          #(base_data, 'job_electron_2012c_Jan2012rereco', 400),
          #(base_data, 'job_electron_2012d_Jan22rereco', 400),

           #(base_phA, 'job_photon_2012a_Jan22rereco', 100),
           #(base_phB, 'job_fall13_photonRunB2012_1',  20),
           #(base_phB, 'job_fall13_photonRunB2012_10', 20),
           #(base_phB, 'job_fall13_photonRunB2012_11', 20),
           #(base_phB, 'job_fall13_photonRunB2012_12', 20),
           #(base_phB, 'job_fall13_photonRunB2012_13', 20),
           #(base_phB, 'job_fall13_photonRunB2012_14', 20),
           #(base_phB, 'job_fall13_photonRunB2012_15', 20),
           #(base_phB, 'job_fall13_photonRunB2012_16', 20),
           #(base_phB, 'job_fall13_photonRunB2012_17', 20),
           #(base_phB, 'job_fall13_photonRunB2012_2',  20),
           #(base_phB, 'job_fall13_photonRunB2012_3',  20),
           #(base_phB, 'job_fall13_photonRunB2012_4',  20),
           #(base_phB, 'job_fall13_photonRunB2012_5',  20),
           #(base_phB, 'job_fall13_photonRunB2012_6',  20),
           #(base_phB, 'job_fall13_photonRunB2012_7',  20),
           #(base_phB, 'job_fall13_photonRunB2012_8',  20),
           #(base_phB, 'job_fall13_photonRunB2012_9',  20),

           #(base_phD, 'job_2photon_2012d_Jan22rereco_1of4', 100),
           #(base_phD, 'job_2photon_2012d_Jan22rereco_2of4', 100),
           #(base_phD, 'job_2photon_2012d_Jan22rereco_3of4', 100),
           (base_phD2, 'job_2photon_2012d_Jan22rereco_4of4', 100),
           (base_phD2, 'job_2photon_2012d_Jan22rereco_5of5', 100),

]

output = 'FilteredSamplesMar14'
nproc=12
exename='RunAnalysisData'

base_cmd = 'python scripts/filter.py  --files root://eoscms/%(base)s/%(job)s.root  --outputDir /tmp/jkunkle/%(job)s  --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfFilter.py --enableRemoveFilter --nsplit %(nsp)d --storagePath /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s --confFileName analysis_config_%(job)s.txt --nproc %(nproc)d --exeName %(exename)s ; python ../../Util/scripts/copy_histograms.py --file root://eoscms/%(base)s/%(job)s.root  --output /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s ; python ../../Util/scripts/clean_conf_files.py --path /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s'

for base, name, nsp in job_conf :

    command = base_cmd %{ 'base' : base, 'job' : name, 'nsp' : nsp, 'output' : output, 'nproc' : nproc, 'exename' : exename } 
    print command
    os.system( command )
