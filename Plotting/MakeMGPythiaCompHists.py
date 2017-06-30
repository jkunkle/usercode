"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()

                                                                                       
p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',         help='base directory for histograms')
p.add_argument('--dirNameMG',     default=None,  type=str ,        dest='dirNameMG',         help='base directory for histograms')
p.add_argument('--dirNamePythia',     default=None,  type=str ,        dest='dirNamePythia',         help='base directory for histograms')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')

options = p.parse_args()

import sys
import os
import re
import ROOT

from SampleManager import SampleManager

if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)

def main() :

    sampMan   = SampleManager(options.baseDir, filename='validation.root', readHists=True)

    samples_lepnu = []
    samples_qq = []

    samples_mg = add_samples_from_dir( sampMan, options.baseDir, options.dirNameMG, 'ChargedResonance' )
    samples_pythia = add_samples_from_dir( sampMan, options.baseDir, options.dirNamePythia, 'PythiaChargedResonance' )

    samples_pythia['qq'] = samples_pythia['lepnu']


    draw_comp_hists( sampMan, 'm_lep_nu_ph', samples_mg['lepnu'], samples_pythia['lepnu'], prefix='MGPythiaCompare_ChargedResonance_WGToLNu', xlabel='Resonance Mass [GeV]' )
    draw_comp_hists( sampMan, 'm_q_q', samples_mg['qq'], samples_pythia['qq'], prefix='MGPythiaCompare_ChargedResonance_WGToJJ', xlabel='Resonance Mass [GeV]' )


def draw_comp_hists( sampMan, var, samples_mg, samples_pythia, prefix, xlabel) :

    ylabel = 'Events'
    logy=True

    all_masses = []
    all_widths = []

    for samp in samples_pythia :
        all_masses.append( samp['mass'] ) 
        all_widths.append( samp['width'] ) 

    all_masses = list( set( all_masses ) )
    all_widths = list( set( all_widths ) )

    for mass in all_masses :

        for width in all_widths :

            for samp in samples_mg + samples_pythia :
                if samp['mass'] == mass and samp['width'] == width :
                    sampMan.activate_sample( samp['name'] )
                else :
                    sampMan.deactivate_sample( samp['name'] )

            xmin = 0
            xmax = 4000

            #xmin = mass / 2
            xmax = mass*1.5

            #if mass >= 1000 :
            #    xmin = mass/1.3
            #    xmax = mass*1.2

            #xmax = mass + 4*(mass/10)
            #xmin = mass - 5*(mass/10)

            rebin = 2
            if mass >  1400 :
                rebin = 4

            #ymax = 500000
            ymax = 5
            ymin = 0.0001

            sampMan.DrawHist( var, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : None, 'labelLoc' : 'topright', 'extra_label' : 'Generated Mass = %d GeV, Width = %s' %(mass,width), 'extra_label_loc' : (0.15, 0.93) }, legend_config={'legendWiden' : 2.5, 'legendCompress' : 0.7, 'entryWidth' : 0.07, 'legendTranslateX' : 0.035}, logy=logy, ymin = ymin, ymax=ymax, xmin=xmin, xmax=xmax, rebin=rebin, normalize=1 )

            if options.outputDir is not None :
                width_name = width
                if width == '0.01' :
                    width_name = width.replace( '.', 'p' )
                name = '%s_M%d_W%s.pdf' %(prefix, mass, width_name )
                sampMan.SaveStack( name, options.outputDir, 'base' )
            else :
                raw_input('continue')

def add_samples_from_dir( sampMan, basepath, subdirname, baseName ) :

    samples = { 'lepnu' : [], 'qq' : [] }

    for dirname in os.listdir( basepath + '/' + subdirname ) :
        res = re.match( '%s_(WGToLNu|WGToJJ)_M(\d{3,4})_width(0p01|\d{1,2})' %baseName , dirname )

        if res is not None :

            mass = int( res.group(2) )
            print dirname
            print res.group(3)
            if res.group(3) == '0p01' :
                width = '0.01'
            else :
                width = res.group(3)

            if res.group(1) == 'WGToLNu' :
                samples['lepnu'].append( {'name' : dirname, 'mass' : mass, 'width' :  width} )
            elif res.group(1) == 'WGToJJ'  :
                samples['qq'].append( {'name' : dirname, 'mass' : mass, 'width' :  width} )

            color = ROOT.kBlack
            if baseName.count('Pythia') :
                color = ROOT.kRed

            sampMan.AddSample( dirname, path='%s/%s' %(subdirname, dirname), isActive=False, isSignal=True, sigLineStyle=1, sigLineWidth=1, plotColor=color )

    return samples

main()
