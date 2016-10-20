import os
import re

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--proc_dir', dest='proc_dir', required=True , help='Path to proc directory (genproductions/bin/MadGraph5_aMCatNLO/)' )
parser.add_argument( '--card_dir', dest='card_dir', required=True , help='Path to card directory relative to proc directory' )
parser.add_argument( '--masses', dest='masses', default=None , help='comma separated list of masses' )
parser.add_argument( '--lepOnly', dest='lepOnly', default=False, action='store_true', help='only run the lepton final state' )
parser.add_argument( '--hadOnly', dest='hadOnly', default=False, action='store_true', help='only run the hadronic final state' )
parser.add_argument( '--checkExisting', dest='checkExisting', default=False, action='store_true', help='Dont run if the gridpack exists' )

options = parser.parse_args()

BASE_NAME = 'ChargedResonance'
#ALL_WIDTHS = ['width10', 'width1', 'width20', 'width5'] 
ALL_WIDTHS = ['width0p01'] 

def main() :

    accept_masses = []
    if options.masses is not None :
        accept_masses = [ int(x) for x in options.masses.split(',')]

    all_cards = []

    for dirname in os.listdir( options.proc_dir+'/'+options.card_dir ) :
        res = re.match( '%s_(WGToLNu|WGToJJ)_M(\d{3,4})' %( BASE_NAME ), dirname )
        if res is not None :
            if accept_masses :
                dirmass = int(res.group( 2 ))

                if dirmass not in accept_masses :
                    continue

            if options.lepOnly and res.group(1) == 'WGToJJ'  :
                continue
            if options.hadOnly and res.group(1) == 'WGToLNu'  :
                continue


            all_cards.append( dirname )

    for card in all_cards :

        for width in ALL_WIDTHS :


            if options.checkExisting :
                output_path = 'Gridpacks/%s_%s_tarball.tar.xz' %(  card, width ) 

                if os.path.isfile( output_path ) :
                    print 'Skipping existing gripack ', output_path
                    continue


            commands = []

            commands.append( 'cd %s' %options.proc_dir )
            commands.append( './gridpack_generation_exo_%s.sh  %s %s/%s ' %( width, card, options.card_dir, card ) )
            commands.append( 'cd ../../..'  )
            commands.append( 'rm -rf %s/%s ' %( options.proc_dir, card ) )
            commands.append( 'mv %s/%s.log Gridpacks/%s_%s.log' %( options.proc_dir, card, card, width ) )
            commands.append( 'mv %s/%s_tarball.tar.xz Gridpacks/%s_%s_tarball.tar.xz' %( options.proc_dir, card, card, width ) )

            all_commands = ' ; '.join( commands )

            print all_commands

            os.system( all_commands )

main()
