import sys

try :
    import cx_Oracle
except ImportError :
    print 'Could not import cx_Oracle!  See README for instructions on the proper setup'
    sys.exit(-1)



class DBManager :

    def __init__( self, conn_str ) :

        print 'Connecting to DB....'

        self.dbConn   = cx_Oracle.connect(conn_str) 
        self.dbCursor = self.dbConn.cursor()

        self.owner_str = 'CMS_HCL_HCAL_COND'

        print 'Connection established, you\'re good to go!'

    def getQuery( self, query ) :

        self.dbCursor.execute( query )
        return self.dbCursor.fetchall()


    def getColumnsInTable( self, table) :

        result = self.getQuery( 'select column_name from all_tab_cols where owner=\'%s\' and table_name=\'%s\' ' %( self.owner_str, table ) )

        for res in result :
            print res[0]

    def raw_query( self, query ) :
        print self.getQuery( query )


        


