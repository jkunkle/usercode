from core import Filter

def get_remove_filter() :
    """ Define list of regex strings to filter input branches to remove from the output.
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableRemoveFilter on the command line.
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return []

def get_keep_filter() :
    """ Define list of regex strings to filter input branches to retain in the output.  
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableKeepFilter on the command line
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return []

def config_analysis( alg_list ) :
    """ Configure analysis modules. Order is preserved """


    raddam_channels = [
                  (-30,35,1),
                  (-30,71,1),
                  (-32,15,1),
                  (-32,51,1),
                  (-34,35,1),
                  (-34,71,1),
                  (-36,15,1),
                  (-36,51,1),
                  (-38,35,1),
                  (-38,71,1),
                  (-40,15,1),
                  (-40,51,1),
                  (-41,35,1),
                  (-41,71,1),
                  (30,21,1),
                  (30,57,1),
                  (32,1,1),
                  (32,37,1),
                  (34,21,1),
                  (34,57,1),
                  (36,1,1),
                  (36,37,1),
                  (38,21,1),
                  (38,57,1),
                  (40,35,1),
                  (40,71,1),
                  (41,19,1),
                  (41,55,1),
                  (-30,15,2),
                  (-30,51,2),
                  (-32,35,2),
                  (-32,71,2),
                  (-34,15,2),
                  (-34,51,2),
                  (-36,35,2),
                  (-36,71,2),
                  (-38,15,2),
                  (-38,51,2),
                  (-40,35,2),
                  (-40,71,2),
                  (-41,15,2),
                  (-41,51,2),
                  (30,1,2),
                  (30,37,2),
                  (32,21,2),
                  (32,57,2),
                  (34,1,2),
                  (34,37,2),
                  (36,21,2),
                  (36,57,2),
                  (38,1,2),
                  (38,37,2),
                  (40,19,2),
                  (40,55,2),
                  (41,35,2),
                  (41,71,2),
                  ]

    raddam_eta   = ''
    raddam_phi   = ''
    raddam_depth = ''

    for ieta, iphi, depth in raddam_channels :

        raddam_eta   +='%s,' %ieta
        raddam_phi   +='%s,' %iphi
        raddam_depth +='%s,' %depth
  

    analysis = Filter('RunAnalysis')
    
    analysis.add_var( 'raddam_eta'  , raddam_eta   )
    analysis.add_var( 'raddam_phi'  , raddam_phi   )
    analysis.add_var( 'raddam_depth', raddam_depth )

    alg_list.append( analysis )


