import os
import re
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--widthsHad', dest='widthsHad', default=None, help='comma separated list of widths to produce for hadronic samples' )
parser.add_argument( '--widthsLep', dest='widthsLep', default=None, help='comma separated list of widths to produce for leptonic samples' )
parser.add_argument( '--nevtHad', dest='nevtHad', default=20000, help='Number of events to run for hadronic samples' )
parser.add_argument( '--nevtLep', dest='nevtLep', default=20000, help='Number of events to run for leptonic samples' )
parser.add_argument( '--hadOnly', dest='hadOnly', default=False, action='store_true', help='make the list for only hadronic samples' )
parser.add_argument( '--lepOnly', dest='lepOnly', default=False, action='store_true', help='make the list for only leptonic samples' )

options = parser.parse_args()

BASE_NAME = 'ChargedResonance'
PWD = os.path.dirname(os.path.realpath(__file__))

def main() :

    selected_gp = []

    for gp in os.listdir( '%s/../Gridpacks' %PWD ) : 

        res = re.match( '(%s_(WGToLNu|WGToJJ)_M(\d{3,4})_width(\d{1,2}|\dp\d{2}))_tarball.tar.xz' %( BASE_NAME ), gp )

        if res is not None :

            if options.hadOnly and res.group(2) == 'WGToLNu' :
                continue
            if options.lepOnly and res.group(2) == 'WGToJJ' :
                continue

            if res.group(2) == 'WGToLNu' and options.widthsLep is not None :
                matches_width_lep = False
                for testw in options.widthsLep.split(',') :
                    if res.group(4) == testw :
                        matches_width_lep = True
                        break
                if not matches_width_lep :
                    continue

            if res.group(2) == 'WGToJJ' and options.widthsHad is not None :
                matches_width_had = False
                for testw in options.widthsHad.split(',') :
                    if res.group(4) == testw :
                        matches_width_had = True
                        break
                if not matches_width_had :
                    continue


            selected_gp.append( ( int(res.group(3)), gp, res.group(1) ) )

    selected_gp.sort()

    for mass, gp, name in selected_gp :

        row_entries = []

        row_entries.append( name )
        if name.count( 'WGToJJ' ) :
            row_entries.append( str( options.nevtHad ) )
        if name.count( 'WGToLNu' ) :
            row_entries.append( str( options.nevtLep ) )

        name_no_width = name[:name.find( '_width') ]

        row_entries.append( 'Hadronizer_TuneCUETP8M1_13TeV_generic_LHE_pythia8_cff.py' )
        row_entries.append( 'Madgraph' )
        row_entries.append( '%s/Gridpacks/%s' %( '/'.join(PWD.split('/')[:-1]), gp ) )
        row_entries.append( 'https://github.com/jkunkle/usercode/tree/master/Gridpacks/ChargedResonance/%s' %name_no_width )

        row = ' , '.join( row_entries )

        print row



main()
