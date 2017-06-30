from argparse import ArgumentParser
import pickle
import os

parser = ArgumentParser()

parser.add_argument( '--baseDir', dest='baseDir', required=True, help='path to directory containting systematics file' )
parser.add_argument( '--electron', dest='electron', default=False, action='store_true', help='do electron modification' )

options = parser.parse_args()


def main() :

    if options.electron :
        ModifyElectron()
    else :
        ModifyJet()

def ModifyElectron() :

    ff_name      = 'results.pickle'
    ff_name_orig = 'results_orig.pickle'

    # first copy the original file
    # so we don't overwrite it
    os.system( 'mv %s/%s %s/%s ' %( options.baseDir, ff_name, options.baseDir, ff_name_orig  ) )

    ofile_orig = open( '%s/%s' %( options.baseDir, ff_name_orig ) )

    ff_dic = pickle.load( ofile_orig )

    ofile_orig.close()

    new_dic = {}
    new_dic['fake_ratio'] = dict( ff_dic['fake_ratio'] )

    new_entries = [ 
                    ( ('40', '1000000'), ('35', '1000000') ), 
                    ( ('40', '70'), ('35', '40') ), 
                    ( ('40', '70'), ('35', '70') ), 
                    #( ('40', 'max'), ('35', 'max') ), 
                    #( ('25', '40') , ('35', '40') ), 
                    #( ('40', '70') , ('35', '70') ), 
    ]

    for key, ff in ff_dic['fake_ratio'].iteritems() : 

        ptmin = key[0]
        ptmax = key[1]


        for ent1, ent2 in new_entries :
            if ptmin == ent1[0] and ptmax == ent1[1] :

                new_key = ( ent2[0], ent2[1], key[2], key[3] )
                print 'Replace %s with %s' %( key, new_key )
                new_dic['fake_ratio'][new_key] = ff_dic['fake_ratio'][key]


    outfile = open( '%s/%s' %( options.baseDir, ff_name ), 'w' )
    pickle.dump( new_dic, outfile )
    outfile.close()



def ModifyJet() :

    syst_name      = 'systematics.pickle'
    syst_name_orig = 'systematics_orig.pickle'

    # first copy the original file
    # so we don't overwrite it
    os.system( 'mv %s/%s %s/%s ' %( options.baseDir, syst_name, options.baseDir, syst_name_orig  ) )

    ofile_orig = open( '%s/%s' %( options.baseDir, syst_name_orig ) )

    syst_dic = pickle.load( ofile_orig )

    ofile_orig.close()

    new_dic = dict( syst_dic )

    new_entries = [ 
                    #( ('25', 'max'), ('20', 'max') ), 
                    #( ('25', '40'), ('20', '40') ), 
                    #( ('25', '70'), ('20', '70') ), 
                    ( ('40', 'max'), ('35', 'max') ), 
                    ( ('25', '40') , ('35', '40') ), 
                    ( ('40', '70') , ('35', '70') ), 
    ]

    for key, vardic in syst_dic.iteritems() : 

        for syst_type, type_dic in vardic.iteritems() :

            for reg, reg_dic in type_dic.iteritems() :
                for ent1, ent2 in new_entries :
                    if ent1 in reg_dic :
                        print 'Copy %s to %s ' %( ent1, ent2 )
                        new_dic[key][syst_type][reg][ent2] = syst_dic[key][syst_type][reg][ent1]


    outfile = open( '%s/%s' %( options.baseDir, syst_name ), 'w' )
    pickle.dump( new_dic, outfile )
    outfile.close()


main()
