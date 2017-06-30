
import os
import pickle
from utils import latex_table

from argparse import ArgumentParser 


parser = ArgumentParser() 

parser.add_argument( '--baseDir', default=None, required=True, dest='baseDir', help='Path to top dir' )


options = parser.parse_args()



def main() :

    for dir in os.listdir( options.baseDir ) :

        if not os.path.isdir( '%s/%s' %( options.baseDir,dir) ) :
            continue

        for file in os.listdir( '%s/%s' %( options.baseDir, dir )  ) :

            if file.count( 'pickle' ) :

                ofile = open( '%s/%s/%s' %( options.baseDir, dir, file ) )

                info = pickle.load( ofile ) 
                ofile.close()


                fbase = file.split('.')[0]

                tab = latex_table()
                #tab.header = '\\documentclass[12pt]{article} \n\n \\usepackage{color} \n \\begin{document} \n\n \\begin{table} \n \\begin{tabular}{| l | c | c || c || c | c |} \hline \n Processes & \multicolumn{2}{|c|}{Efficiencies} & Normalization &  \multicolumn{2}{|c|}{Predictions} ' + r'  \\ \hline ' + '\n' + '  & Tight & Loose &      & Tight  &  Loose   ' + r'  \\ \hline '
                tab.header = '\\begin{table} \n \\begin{tabular}{| l | c | c || c || c | c |} \hline \n Processes & \multicolumn{2}{|c|}{Efficiencies} & Normalization &  \multicolumn{2}{|c|}{Predictions} ' + r'  \\ \hline ' + '\n' + '  & Tight & Loose &      & Tight  &  Loose   ' + r'  \\ \hline '

                tab.add_row( 'Real', [ '%.2f' %info['efficiencies']['eff_R_T'].n, '%.2f' %info['efficiencies']['eff_R_L'].n, '${:.2ufL}$'.format(info['alphas']['R']), '${:.2ufL}$'.format(info['results']['p_R_T']) , '${:.2ufL}$'.format(info['results']['p_R_L']) ] )
                tab.add_row( 'Fake', [ '%.2f' %info['efficiencies']['eff_F_T'].n, '%.2f' %info['efficiencies']['eff_F_L'].n, '${:.2ufL}$'.format(info['alphas']['F']) , '\color{red}' + '${:.2ufL}$'.format(info['results']['p_F_T']) , '${:.2ufL}$'.format(info['results']['p_F_L']) ] )
                tab.add_divider()
                tab.add_row( 'Data', [ '${:.2ufL}$'.format(info['data']['T']), '${:.2ufL}$'.format(info['data']['L']), '\multicolumn{3}{|c|}{}'] )

                #tab.footer = '\\end{tabular} \n \\end{table} \n \\end{document}'
                tab.footer = '\\end{tabular} \n \\end{table} '

                tab.write( '%s/%s/%s.tex' %( options.baseDir, dir, fbase ) )

                #os.system( 'cd %s/%s ; pdflatex %s.tex ; cd - ' %( options.baseDir, dir, fbase ) )




main()

