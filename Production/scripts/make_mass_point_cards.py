import os
import re

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--original_cards', dest='original_cards', required=True, help='path to start from' )
parser.add_argument( '--output_dir', dest='output_dir', required=True, help='location to write new directories' )

options = parser.parse_args()

#mass_points = [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500, 4000]
mass_points = [3500, 4000]

base_name = 'ChargedResonance_WGToLNu'
#base_name = 'ChargedResonance_WGToJJ'

def main() :


    for mass_point in mass_points :

        # this is the new directory name
        dir_name = '%s_M%d' %( base_name, mass_point)

        dir_path = '%s/%s' %( options.output_dir, dir_name )

        # make the directory if it hasn't been made
        # note that if the directory exists it'll be overwritten
        if not os.path.isdir( dir_path ) :
            os.mkdir( dir_path )

        # find the mass point of the original directory
        original_name = options.original_cards.rstrip('/').split('/')[-1]
        original_mass = int(re.match( '%s_M(\d{3,4})' %base_name, original_name ).group(1))


        # copy the cards over, modifying the mass point in the name
        for card_file in os.listdir( options.original_cards ) :

            new_file = card_file.replace( str(original_mass), str( mass_point ) )

            os.system( 'cp %s/%s %s/%s/%s' %( options.original_cards, card_file, options.output_dir, dir_name, new_file ) )

            # modify the mass in the customize_card
            if card_file.count( 'customizecards' ) :
                tmp_cust_card = new_file + '.save'

                os.system( 'mv %s/%s/%s %s/%s/%s ' %( options.output_dir, dir_name, new_file, options.output_dir, dir_name, tmp_cust_card ) )

                infile = open( '%s/%s/%s' %( options.output_dir, dir_name, tmp_cust_card ), 'r' )
                outfile = open( '%s/%s/%s' %( options.output_dir, dir_name, new_file ), 'w' )

                for line in infile :

                    if line.count( '9000007')  :
                        outfile.write( 'set param_card mass 9000007 %f \n' %( float( mass_point ) ) )
                    else :
                        outfile.write( '%s' %line )

                infile.close()
                outfile.close()


            # modify the output in the proc_card
            if card_file.count( 'proc_card' ) :

                tmp_proc_card = new_file + '.save'

                os.system( 'mv %s/%s/%s %s/%s/%s ' %( options.output_dir, dir_name, new_file, options.output_dir, dir_name, tmp_proc_card ) )

                infile = open( '%s/%s/%s' %( options.output_dir, dir_name, tmp_proc_card ), 'r' )
                outfile = open( '%s/%s/%s' %( options.output_dir, dir_name, new_file ), 'w' )

                for line in infile :
                    if line.count('output') > 0 :
                        outfile.write( 'output %s \n' %( dir_name ) )
                    else :
                        outfile.write( line )

                infile.close()
                outfile.close()

                        
                




main()

