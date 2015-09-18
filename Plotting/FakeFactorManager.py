import os
import pickle

class FakeFactorManager :

    def __init__(self, file, access_path=[] ) :

        if not os.path.isfile( file )  :
            print 'FakeFactorManager::init -- ERROR file %s does not exist' %file
            self.ff_dict = {}

        else :
            ofile = open( file )
            file_dict = pickle.load( ofile )
            ofile.close()

            # if the fake factors are buried within the dict
            # use the access path to
            # get to the fake factors 
            if not access_path :
                self.ff_dict = file_dict
            else :

                # first make some formatting changes
                mod_fields = []
                for field in access_path :
                    if isinstance( field, str ) :
                        mod_fields.append( '\'%s\'' %field )
                    elif isinstance( field, tuple ) :
                        mod_fields.append( '%s' %(field,) )
                    else :
                        mod_fields.append(field)

                eval_path = 'file_dict[' + ']['.join( mod_fields ) + ']'
                
                try :
                    self.ff_dict = eval(eval_path)
                except :
                    print 'Dict access path was not correct'
                    raise

        # figure out if pt or eta comes first 
        # get the maximum values of the
        # second of each pt or eta entry
        # and assume that the one with the greater
        # value is pt
        self.pt_first = None
        second_entries = []
        fourth_entries = []
        for bin in self.ff_dict :
            second_entries.append( float( bin[1] ) )
            fourth_entries.append( float( bin[3] ) )

        print self.ff_dict
        max_second = max( second_entries )
        max_fourth = max( fourth_entries )

        if max_second > max_fourth :
            self.pt_first = True
        else :
            self.pt_first = False

    def get_pt_eta_ff( self, ptmin, ptmax, etamin, etamax ) :

        if self.pt_first :
            return self._get_ff( ptmin, ptmax, etamin, etamax )
        else :
            return self._get_ff( etamin, etamax, ptmin, ptmax)
    def _get_ff( self, ent1min, ent1max, ent2min, ent2max) :

        if ent1max == 'max' :
            all_1max = []
            for key in self.ff_dict.keys() :
                all_1max.append( float(key[1]) )
            ent1max = max( all_1max )
        if ent2max == 'max' :
            all_2max = []
            for key in self.ff_dict.keys() :
                all_2max.append( float(key[3]) )
            ent2max = max( all_2max )

        for key, val in self.ff_dict.iteritems() :

            min1 = float(key[0])
            max1 = float(key[1])
            min2 = float(key[2])
            max2 = float(key[3])

            #print 'ent  min, max = %s, %s, %s, %s ' %( ent1min, ent1max, ent2min, ent2max) 
            #print 'dict min, max = %s, %s, %s, %s ' %( min1, max1, min2, max2)

            if float(ent1min) == min1 and float(ent1max) == max1 and float(ent2min) == min2 and float(ent2max) == max2 :
                return val

        print 'Could Not locate FF for entries %s, %s, %s, %s' %( ent1min, ent1max, ent2min, ent2max)
        print self.ff_dict.keys()
        return -1


