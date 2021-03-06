import sys
import os

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('--packageName', dest='packageName', default=None, required=True, help='Name of new package (required)' )

options = parser.parse_args()

#We're just gonna copy the Template directory to the name given to --packageName
print 'Copy Template directory to %s' %options.packageName
if not os.path.isdir( options.packageName ) :
    os.system('cp -r Template %s' %options.packageName )
else :
    print 'ERROR -- Target directory already exists!'
    sys.exit()

print 'Enter new package and run a small analysis to create first generated c++ code '
print ('cd %s ; echo "PACKAGE=%s">&Makefile ; echo "include ../Makefile.global">>Makefile ; python scripts/filter.py  --files test/tree.root --fileKey tree.root --outputDir /tmp --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfTemplate.py ; rm scripts/ConfTemplate.pyc ; cd .. ' %( options.packageName, options.packageName ) )
os.system('cd %s ; echo "PACKAGE=%s">&Makefile ; echo "include ../Makefile.global">>Makefile ; python scripts/filter.py  --files test/tree.root --fileKey tree.root --outputDir /tmp --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfTemplate.py ; rm scripts/ConfTemplate.pyc ; cd .. ' %( options.packageName, options.packageName ) )



print 'If the above job compiled and ran successfully, you\'re good to go! ^.^'


