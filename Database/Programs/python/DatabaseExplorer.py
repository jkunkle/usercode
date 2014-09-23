import sys
import os
from argparse import ArgumentParser
import ROOT

#try :
#    import cx_Oracle
#except ImportError :
#    print 'Could not import cx_Oracle!  See README for instructions on the proper setup'
#    sys.exit(-1)

from DBManager import DBManager

dbMan=None

def main() :
    """ main function -- runs first """

    global dbMan
    dbMan = DBManager( 'CMS_HCL_APPUSER_R/HCAL_Reader_55@localhost:1521/cms_omds_lb.cern.ch' )


def help() :
    """ Display information on available functions """ 

    import types

    globs = globals()
    for key, val in globs.iteritems() :
        if isinstance(val, types.FunctionType ) :
            print key
    #for obj in globals() :
    #    print obj
    #    print obj.callable()
    print globals()['main'].__doc__



def getListOfGOLConfigs() :
    """ List all GOL configuration sets """

    global dbMan

    print dbMan.getQuery( 'select unique NAME_LABEL from CMS_HCL_HCAL_COND.V_HCAL_RBX_GOL_CONFIG' )


def plotGOLConfig( config_name=None, det_slice=None ) :
    pass


main()
