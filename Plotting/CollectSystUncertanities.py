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

    id_vars =['sigmaIEIE', 'chIsoCorr', 'neuIsoCorr', 'phoIsoCorr' ]
    _pt_order = [('15', '25'), ('25', '40'), ('40', '70'), ('70', 'max') ]

    all_syst = {}

    # format of key changes for different variables
    fake_nom_file_keys = { 'sigmaIEIE' : 'ph_sigmaIEIE__(?P<reg>EB|EE)__mmg__Zgammastar__Compph_chIsoCorrcuts__pt_(?P<pt1>\d+)-(?P<pt2>\d+|max)__varBins.pickle',
                           'chIsoCorr' : 'ph_chIsoCorr__(?P<reg>EB|EE)__mmg__Zgammastar__Compph_sigmaIEIEcuts__pt_(?P<pt1>\d+)-(?P<pt2>\d+|max)__varBins.pickle',
                           'neuIsoCorr' : 'ph_neuIsoCorr__(?P<reg>EB|EE)__mmg__Zgammastar__Compph_sigmaIEIEcuts__pt_(?P<pt1>\d+)-(?P<pt2>\d+|max)__varBins.pickle',
                           'phoIsoCorr' : 'ph_phoIsoCorr__(?P<reg>EB|EE)__mmg__Zgammastar__Compph_sigmaIEIEcuts__pt_(?P<pt1>\d+)-(?P<pt2>\d+|max)__varBins.pickle',
                         }
    fake_nom_file_keys_inc = { 'sigmaIEIE' : 'ph_sigmaIEIE__(?P<reg>EB|EE)__mmg__Zgammastar__Compph_chIsoCorrcuts__pt_15-max__varBins.pickle',
                           'chIsoCorr' : 'ph_chIsoCorr__(?P<reg>EB|EE)__mmg__Zgammastar__Compph_sigmaIEIEcuts__pt_15-max__varBins.pickle',
                           'neuIsoCorr' : 'ph_neuIsoCorr__(?P<reg>EB|EE)__mmg__Zgammastar__Compph_sigmaIEIEcuts__pt_15-max__varBins.pickle',
                           'phoIsoCorr' : 'ph_phoIsoCorr__(?P<reg>EB|EE)__mmg__Zgammastar__Compph_sigmaIEIEcuts__pt_15-max__varBins.pickle',
                         }
    fake_nom_ratio_keys = { 'sigmaIEIE' : '5 < Iso < 10',
                            'chIsoCorr' : '#sigma i#etai#eta > 0.0(\d+)',
                            'neuIsoCorr' : '#sigma i#etai#eta > 0.0(\d+)',
                            'phoIsoCorr' : '#sigma i#etai#eta > 0.0(\d+)',
                          }

    fake_asym_ratio_keys = { 'sigmaIEIE' : '(\d+),(\d+),(\d+)\s*\(ch,neu,pho\)',
                             'chIsoCorr' : 'No Cut,(\d+),(\d+)\s*\(ch,neu,pho\)',
                             'neuIsoCorr' : '(\d+),No Cut,(\d+)\s*\(ch,neu,pho\)',
                             'phoIsoCorr' : '(\d+),(\d+),No Cut\s*\(ch,neu,pho\)',
                           }

    for var in id_vars :
        all_syst[var] = {}

        file_key_jet_temp_fake_nom  = 'ph_%s__(?P<reg>EB|EE)__mmg__Zgammastar__Compph_chIsoCorrcuts__pt_(?P<pt1>\d+)-(?P<pt2>\d+|max)__varBins.pickle' %var
        file_key_jet_temp_fake_asym = 'ph_%s__(?P<reg>EB|EE)__mmg__Zgammastar__pt_(?P<pt1>\d+)-(?P<pt2>\d+|max)__CompLoosenedIsoCuts__varBins.pickle'  %var
        file_key_jet_temp_real_nom  = 'ph_%s__(?P<reg>EB|EE)__pt_(?P<pt1>\d+)-(?P<pt2>\d+|max)__CompDataRealPhotonMCTruthMatchPhoton__varBins.pickle'  %var

        file_key_jet_temp_fake_nom_inc  = 'ph_%s__(?P<reg>EB|EE)__mmg__Zgammastar__pt_15-max__Compph_chIsoCorrcuts__varBins.pickle' %var
        file_key_jet_temp_fake_asym_inc = 'ph_%s__(?P<reg>EB|EE)__mmg__Zgammastar__pt_15-max__CompLoosenedIsoCuts__varBins.pickle'  %var
        file_key_jet_temp_real_inc      = 'ph_%s__(?P<reg>EB|EE)__pt_15-max__CompDataRealPhotonMCTruthMatchPhoton__varBins.pickle'  %var

        sub_dir_jet = options.baseDir+'/JetFakeTemplatePlots'


        files_jet_temp_fake_nom  = find_files_in_dir( sub_dir_jet, fake_nom_file_keys[var] )
        files_jet_temp_real_nom  = find_files_in_dir( sub_dir_jet, file_key_jet_temp_real_nom  )
        files_jet_temp_fake_asym = find_files_in_dir( sub_dir_jet, file_key_jet_temp_fake_asym )


        files_jet_temp_fake_nom_inc  = find_files_in_dir( sub_dir_jet, fake_nom_file_keys_inc[var] )
        files_jet_temp_real_inc      = find_files_in_dir( sub_dir_jet, file_key_jet_temp_real_inc      )
        files_jet_temp_fake_asym_inc = find_files_in_dir( sub_dir_jet, file_key_jet_temp_fake_asym_inc )

        ratio_key_temp_fake_nom = '5 < Iso < 10'
        ratio_key_temp_fake_asym = '(\d+|No Cut),(\d+|No Cut),(\d+|No Cut)\s*\(ch,neu,pho\)'
        ratio_key_temp_real = 'W#gamma, truth matched photons'

        data_temp_fake_nom = {}
        dat_temp_fake_asym = {}
        syst_temp_real = {}

        data_temp_fake_nom  = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_fake_nom, fake_nom_ratio_keys[var])
        data_temp_fake_asym = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_fake_asym, ratio_key_temp_fake_asym)
        data_temp_real_nom  = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_real_nom, ratio_key_temp_real)

        data_temp_fake_nom_inc  = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_fake_nom_inc, fake_nom_ratio_keys[var] )
        data_temp_fake_asym_inc = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_fake_asym_inc, ratio_key_temp_fake_asym)
        data_temp_real_inc      = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_real_inc, ratio_key_temp_real)

        # collect the data for the real
        # templates which have a different
        # file for each isolation value
        iso_vals = [(5,3,3), (8,5,5), (10,7,7), (12,9,9), (15,11,11), (20, 16,16)]
        data_temp_real_asym = {}
        data_temp_real_asym_inc = {}

        all_syst[var]['RealTemplateNom']={}
        all_syst[var]['FakeTemplateNom']={}
        for vals in iso_vals :

            syst_postfix = '%d-%d-%d' %(vals)
            iso_str = 'iso%d-%d-%d' %( vals[0], vals[1], vals[2] )
            if var == 'chIsoCorr' :
                syst_postfix = 'No Cut-%d-%d' %( vals[1], vals[2] )
                iso_str = 'isoNone-%d-%d' %(vals[1], vals[2] )
            elif var == 'neuIsoCorr' :
                syst_postfix = '%d-No Cut-%d' %( vals[0], vals[2] )
                iso_str = 'iso%d-None-%d' %(vals[0], vals[2] )
            elif var == 'phoIsoCorr' :
                syst_postfix = '%d-%d-No Cut' %( vals[0], vals[1] )
                iso_str = 'iso%d-%d-None' %(vals[0], vals[1] )

            all_syst[var]['FakeTemplate'+syst_postfix] = {}
            all_syst[var]['RealTemplate'+syst_postfix] = {}


            file_key_jet_temp_real_asym = 'ph_%s__(?P<reg>EB|EE)__%s__pt_(?P<pt1>\d+)-(?P<pt2>\d+|max)__CompDataRealPhotonMCTruthMatchPhoton__varBins.pickle' %(var, iso_str )
            files_jet_temp_real_asym = find_files_in_dir( sub_dir_jet, file_key_jet_temp_real_asym )
            data_temp_real_asym['RealTemplate'+syst_postfix] = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_real_asym, ratio_key_temp_real)

            file_key_jet_temp_real_asym_inc = 'ph_%s__(?P<reg>EB|EE)__%s__pt_15-max__CompDataRealPhotonMCTruthMatchPhoton__varBins.pickle' %(var, iso_str )
            files_jet_temp_real_asym_inc = find_files_in_dir( sub_dir_jet, file_key_jet_temp_real_asym_inc )
            data_temp_real_asym_inc['RealTemplate'+syst_postfix] = get_data_from_files_with_leg_key( sub_dir_jet, files_jet_temp_real_asym_inc, ratio_key_temp_real )


        # combine pt dependent with inclusive
        for reg in data_temp_fake_nom.keys() :
            data_temp_fake_nom[reg][(None,None)] = data_temp_fake_nom_inc[reg][(None,None)]
        for reg in data_temp_fake_asym.keys() :
            data_temp_fake_asym[reg][(None,None)] = data_temp_fake_asym_inc[reg][(None,None)]
        for reg in data_temp_real_nom.keys() :
            data_temp_real_nom[reg][(None,None)] = data_temp_real_inc[reg][(None,None)]
        for iso, iso_data in data_temp_real_asym.iteritems() :
            for reg in iso_data.keys() :
                data_temp_real_asym[iso][reg][(None,None)] = data_temp_real_asym_inc[iso][reg][(None,None)]



        #for reg_vals in data_temp_fake_asym.values() :
        #    for pt_vals in reg_vals.values() :
        #        for isokey in pt_vals.keys() :
        #            res = re.match( ratio_key_temp_fake_asym, isokey )
        #            if res is not None :
        #                all_syst[var]['FakeTemplate%s-%s-%s'%(res.group(1), res.group(2), res.group(3))] = {}

        print '-------------------------'
        print var
        print all_syst[var]
        print '-------------------------'

        #for iso in iso_vals :
        #    all_syst[var]['RealTemplate%s' %(syst_postfix)] = {}

        for reg, reg_data in data_temp_fake_asym.iteritems() :
            for val in all_syst[var].values() :
                val.setdefault(reg, {})
            for pt, pt_data_fake_asym in reg_data.iteritems() :

                if var == 'sigmaIEIE' :
                    for bins in data_temp_fake_nom[reg][pt][ratio_key_temp_fake_nom]['bins'] :
                        if bins['bin'] == 2 :
                            all_syst[var]['FakeTemplateNom'][reg][pt] = math.fabs(1-bins['val'])
                else :
                    if '#sigma i#etai#eta > 0.033 ' in data_temp_fake_nom[reg][pt] :
                        for bins in data_temp_fake_nom[reg][pt]['#sigma i#etai#eta > 0.033 ']['bins'] :
                            if bins['bin'] == 2 :
                                all_syst[var]['FakeTemplateNom'][reg][pt] = math.fabs(1-bins['val'])
                    elif '#sigma i#etai#eta > 0.011 ' in data_temp_fake_nom[reg][pt] :
                        for bins in data_temp_fake_nom[reg][pt]['#sigma i#etai#eta > 0.011 ']['bins'] :
                            if bins['bin'] == 2 :
                                all_syst[var]['FakeTemplateNom'][reg][pt] = math.fabs(1-bins['val'])

                for bins in data_temp_real_nom[reg][pt][ratio_key_temp_real]['bins'] :
                    if bins['bin'] == 2 :
                        all_syst[var]['RealTemplateNom'][reg][pt] = math.fabs(1-bins['val'])

                for iso, pt_data_real_asym in data_temp_real_asym.iteritems() :
                    for bins in pt_data_real_asym[reg][pt][ratio_key_temp_real]['bins'] :
                        if bins['bin'] == 2 :
                            all_syst[var][iso][reg][pt] = math.fabs( 1-bins['val'] )

                for type, type_data in pt_data_fake_asym.iteritems() :
                    res = re.match( ratio_key_temp_fake_asym, type )
                    if res is not None :
                        temp_name = 'FakeTemplate%s-%s-%s' %(res.group(1), res.group(2), res.group(3))
                        for bins in type_data['bins'] :
                            if bins['bin'] == 2 :
                               all_syst[var][temp_name][reg][pt] = math.fabs(1-bins['val'])

        # replace some high pt systematics
        # with those from lower pt regions
        # get ordered pt
        ordered_pt = []
        for ptkey in all_syst[var].values()[0].values()[0].keys() :
            if ptkey[0] is not None :
                if ptkey[1] != 'max' :
                    ordered_pt.append( (int(ptkey[0]), int(ptkey[1]) ) )
                else :
                    ordered_pt.append( (int(ptkey[0]), 'max' ) )

        ordered_pt.sort()
        ordered_pt = [ (str(x[0]),str(x[1])) for x in ordered_pt ]

        # for the real templates systs, 
        # replace 40-80 with 25-40 (ie [-2] with [-3] )
        for type in all_syst[var].keys() :
            if type.count('RealTemplate' ) :
                for reg, reg_data in all_syst[var][type].iteritems() :
                    all_syst[var][type][reg][ordered_pt[-2]] = all_syst[var][type][reg][ordered_pt[-3]]

        # for every syst type, replace 80-max with
        # 40-80 (ie [-1] with [-2]
        for type, type_data in all_syst[var].iteritems() :
            for reg, reg_data in type_data.iteritems() :
                all_syst[var][type][reg][ordered_pt[-1]] = all_syst[var][type][reg][ordered_pt[-2]]


        # don't let higher pt regions have smaller syst than lower pt regions
        for ptidx, pt in enumerate(_pt_order[:-1]) :
            for type, type_data in all_syst[var].iteritems() :
                for reg, reg_data in type_data.iteritems() :
                    if all_syst[var][type][reg][pt] > all_syst[var][type][reg][_pt_order[ptidx+1]] :
                        all_syst[var][type][reg][_pt_order[ptidx+1]] = all_syst[var][type][reg][pt]

    for var in id_vars :
        print 'ID variable %s : ' %var
        for type, type_data in all_syst[var].iteritems() :
            print '%s , %s : '%(var, type)
            for reg, reg_data in type_data.iteritems() :
                print '\t %s : '%reg
                for pt in ordered_pt :
                    if pt in reg_data :
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
