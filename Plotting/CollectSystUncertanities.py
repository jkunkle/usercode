#-----------------------------------------------------
#
# Generate systematic inputs to RunMatrixFit.py
# Real and fake template systematics are 
# taken from variations in 
# sigmaIEIE shape
#
#-----------------------------------------------------


import re
import os
import math
import pickle
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument( '--baseDir', default=None, dest='baseDir', help='Plot Directory'  )
p.add_argument( '--save', default=False, action='store_true', dest='save', help='Save output'  )

options = p.parse_args()

def main() :

    if options.baseDir is None :
        print 'Must provide a base directory'
        return

    file_key_jet_temp_fake_nom  = 'ph_sigmaIEIE__(?P<reg>EB|EE)__mmg__Zgammastar__Compph_chIsoCorrcuts__pt_(?P<pt1>\d+)-(?P<pt2>\d+|max)__varBins.pickle'
    file_key_jet_temp_fake_asym = 'ph_sigmaIEIE__(?P<reg>EB|EE)__mmg__Zgammastar__pt_(?P<pt1>\d+)-(?P<pt2>\d+|max)__CompLoosenedIsoCuts__varBins.pickle'
    file_key_jet_temp_real      = 'ph_sigmaIEIE__(?P<reg>EB|EE)__pt_(?P<pt1>\d+)-(?P<pt2>\d+|max)__CompDataRealPhotonMCTruthMatchPhoton_twoBin.pickle'

    file_key_jet_temp_fake_nom_inc  = 'ph_sigmaIEIE__(?P<reg>EB|EE)__mmg__Zgammastar__Compph_chIsoCorrcuts__varBins.pickle'
    file_key_jet_temp_fake_asym_inc = 'ph_sigmaIEIE__(?P<reg>EB|EE)__mmg__Zgammastar__CompLoosenedIsoCuts__varBins.pickle'
    file_key_jet_temp_real_inc      = 'ph_sigmaIEIE__(?P<reg>EB|EE)__CompDataRealPhotonMCTruthMatchPhoton_twoBin.pickle'

    sub_dir_jet = options.baseDir+'/JetFakeTemplatePlots'

    files_jet_temp_fake_nom  = find_files_in_dir( sub_dir_jet, file_key_jet_temp_fake_nom  )
    files_jet_temp_real      = find_files_in_dir( sub_dir_jet, file_key_jet_temp_real      )
    files_jet_temp_fake_asym = find_files_in_dir( sub_dir_jet, file_key_jet_temp_fake_asym )

    files_jet_temp_fake_nom_inc  = find_files_in_dir( sub_dir_jet, file_key_jet_temp_fake_nom_inc  )
    files_jet_temp_real_inc      = find_files_in_dir( sub_dir_jet, file_key_jet_temp_real_inc      )
    files_jet_temp_fake_asym_inc = find_files_in_dir( sub_dir_jet, file_key_jet_temp_fake_asym_inc )


    ratio_key_temp_fake_nom = '5 < Iso < 10'
    ratio_key_temp_fake_asym = '(\d+),(\d+),(\d+)\s*\(ch,neu,pho\)'
    ratio_key_temp_real = 'W#gamma, truth matched photons'

    data_temp_fake_nom = {}
    dat_temp_fake_asym = {}
    syst_temp_real = {}

    data_temp_fake_nom  = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_fake_nom, ratio_key_temp_fake_nom )
    data_temp_fake_asym = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_fake_asym, ratio_key_temp_fake_asym)
    data_temp_real      = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_real, ratio_key_temp_real)

    data_temp_fake_nom_inc  = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_fake_nom_inc, ratio_key_temp_fake_nom )
    data_temp_fake_asym_inc = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_fake_asym_inc, ratio_key_temp_fake_asym)
    data_temp_real_inc      = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_real_inc, ratio_key_temp_real)

    # combine pt dependent with inclusive
    for reg, reg_data in data_temp_fake_nom.iteritems() :
        data_temp_fake_nom[reg][(None,None)] = data_temp_fake_nom_inc[reg][(None,None)]
    for reg, reg_data in data_temp_fake_asym.iteritems() :
        data_temp_fake_asym[reg][(None,None)] = data_temp_fake_asym_inc[reg][(None,None)]
    for reg, reg_data in data_temp_real.iteritems() :
        data_temp_real[reg][(None,None)] = data_temp_real_inc[reg][(None,None)]

    all_syst = {}
    all_syst['RealTemplateNom']={}
    all_syst['FakeTemplateNom']={}

    for reg_vals in data_temp_fake_asym.values() :
        for pt_vals in reg_vals.values() :
            for isokey in pt_vals.keys() :
                res = re.match( ratio_key_temp_fake_asym, isokey )
                if res is not None :
                    all_syst['FakeTemplate%s-%s-%s'%(res.group(1), res.group(2), res.group(3))] = {}

    for reg, reg_data in data_temp_fake_nom.iteritems() :
        for val in all_syst.values() :
            val.setdefault(reg, {})
        for pt, pt_data_fake_nom in reg_data.iteritems() :
            for val in all_syst.values() :
                val[reg].setdefault(pt, {})

            pt_data_fake_asym = data_temp_fake_asym[reg][pt]
            pt_data_real = data_temp_real[reg][pt]

            for bins in pt_data_fake_nom[ratio_key_temp_fake_nom]['bins'] :
                if bins['bin'] == 2 :
                    all_syst['FakeTemplateNom'][reg][pt] = math.fabs(1-bins['val'])
            for bins in pt_data_real[ratio_key_temp_real]['bins'] :
                if bins['bin'] == 2 :
                    all_syst['RealTemplateNom'][reg][pt] = math.fabs(1-bins['val'])
            for type, type_data in pt_data_fake_asym.iteritems() :
                res = re.match( ratio_key_temp_fake_asym, type )
                if res is not None :
                    temp_name = 'FakeTemplate%s-%s-%s' %(res.group(1), res.group(2), res.group(3))
                    for bins in type_data['bins'] :
                        if bins['bin'] == 2 :
                           all_syst[temp_name][reg][pt] = math.fabs(1-bins['val'])

    # replace some high pt systematics
    # with those from lower pt regions
    # get ordered pt
    ordered_pt = []
    for ptkey in all_syst.values()[0].values()[0].keys() :
        if ptkey[0] is not None :
            if ptkey[1] != 'max' :
                ordered_pt.append( (int(ptkey[0]), int(ptkey[1]) ) )
            else :
                ordered_pt.append( (int(ptkey[0]), 'max' ) )

    ordered_pt.sort()
    ordered_pt = [ (str(x[0]),str(x[1])) for x in ordered_pt ]

    # for the real templates systs, 
    # replace 40-80 with 25-40 (ie [-2] with [-3] )
    for reg, reg_data in all_syst['RealTemplateNom'].iteritems() :
        all_syst['RealTemplateNom'][reg][ordered_pt[-2]] = all_syst['RealTemplateNom'][reg][ordered_pt[-3]]

    # for every syst type, replace 80-max with
    # 40-80 (ie [-1] with [-2]
    for type, type_data in all_syst.iteritems() :
        for reg, reg_data in type_data.iteritems() :
            all_syst[type][reg][ordered_pt[-1]] = all_syst[type][reg][ordered_pt[-2]]

    # don't let higher pt regions have smaller syst than lower pt regions
    for ptidx, pt in enumerate(ordered_pt[:-1]) :
        for type, type_data in all_syst.iteritems() :
            for reg, reg_data in type_data.iteritems() :
                if all_syst[type][reg][pt] > all_syst[type][reg][ordered_pt[ptidx+1]] :
                    all_syst[type][reg][ordered_pt[ptidx+1]] = all_syst[type][reg][pt]

    for type, type_data in all_syst.iteritems() :
        print '%s : '%type
        for reg, reg_data in type_data.iteritems() :
            print '\t %s : '%reg
            for pt in ordered_pt :
                print '\t\t pt %s-%s : %f'%(pt[0], pt[1], reg_data[pt])


    if options.save :
        output_file = sub_dir_jet+'/systematics.pickle'
        ofile = open( output_file, 'w' )
        pickle.dump( all_syst, ofile)
        ofile.close()

def find_files_in_dir( dir, file_key ) :

    out_files = {}

    for file in os.listdir( dir ) :
        res = re.match( file_key, file )

        if res is not None :
            reg = res.group('reg')
            if len(res.groups()) > 2 :
                pt1 = res.group('pt1')
                pt2 = res.group('pt2')
                if int(pt1) < 15 :
                    continue
            else :
                pt1 = None
                pt2 = None
            out_files.setdefault( reg, {} )

            out_files[reg][(pt1,pt2)] = file

    return out_files

def get_data_from_files_with_leg_key( dir, files, leg_key ) :

    output = {}

    for reg, ptfiles in files.iteritems() :
        output.setdefault( reg, {} )
        for pt, file in ptfiles.iteritems() :
            output[reg].setdefault( pt, {} )
            ofile = open('%s/%s' %(dir, file) )
            file_results = pickle.load( ofile )
            ofile.close()
            for key, val in file_results.iteritems() :
                if isinstance( val, dict ) :
                    legend_entry = val.get('legend_entry', None )
                    res = re.match( leg_key, legend_entry )
                    if res is not None :
                        output[reg][pt][legend_entry] = val

    return output



main()
