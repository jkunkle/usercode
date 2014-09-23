#!/usr/bin/env python
"""Removes from eos space root files produced by failed GRID jobs.

   Execution aborts on first encountered error, printing out python's traceback
   information.

   NOTE: no spaces in file names are allowed.
"""

# enable python-3 features
from __future__ import division        # 1/2 = 0.5, not 0
from __future__ import print_function  # print() syntax from python-3

import sys
import subprocess

def main():
    """Steering function.
    """
    # check input / print usage info
    args = sys.argv
    if not (len(args) == 2 or (len(args) == 3 and args[1] == '--pretend')):
        print('Usage: {0} [--pretend] <eosdir>'.format(sys.argv[0]))
        sys.exit(1)

    # input
    indir = sys.argv[-1]

    # get indir contents
    out = command('ls', '-l', indir)
    lines = out.strip().split('\n') # strip() removes '\n' at the end of 'out'

    prefix = set()       # common prefix(es) in names of files
    job_timestamps = {}  # {job: list of timestamps}
    job_resubmits = {}   # {job: list of resubmits}
    job_linenos = {}     # {job: list of entry numbers in 'lines'}

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
              'Oct', 'Nov', 'Dec']

    # fill objects defined above; example of an entry in 'lines':
    # -rw-r--r--  1 konush  zh    161969875 Oct 02 20:09 ggtree_mc_81_1_RJD.root
    for (i, line) in enumerate(lines):
        (month, day, time, filename) = line.split()[-4:]
        (hour, minute) = time.split(':')

        # number of days in a month is not important, only continuity matters
        ndays = months.index(month) * 31 + int(day)
        timestamp = ndays * 24 * 60 + int(hour) * 60 + int(minute)

        # split file name
        (job, resubmits, suff) = filename.split('_')[-3:]

        if not job.isdigit() or len(suff) != 8 or not suff.endswith('.root'):
            raise Exception('invalid file name: ' + filename)

        prefix.add('_'.join(filename.split('_')[:-3]))
        job_timestamps.setdefault(job, []).append(timestamp)
        job_resubmits.setdefault(job, []).append(int(resubmits))
        job_linenos.setdefault(job, []).append(i)

    # check that prefix in names of files is unique
    if len(prefix) > 1:
        string = ' '.join(sorted(prefix))
        raise Exception('file name prefix is not unique: ' + string)

    todel = []  # entry numbers in 'lines' for files to be deleted

    # fill 'todel'
    for job in job_timestamps:
        timestamps = job_timestamps[job]
        resubmits = job_resubmits[job]
        linenos = job_linenos[job]

        # verify that no files with duplicated resubmit number exist
        if len(set(resubmits)) != len(resubmits):
            msg = 'duplicated resubmit number encountered for job ' + job
            raise Exception(msg)

        # latest timestamp and highest resubmit number
        tsmax = max(timestamps)
        resubmax = max(resubmits)

        # verify that no file for same job was created within a minute
        if timestamps.count(tsmax) != 1:
            msg = 'two or more files created within a minute for job ' + job
            raise Exception(msg)

        # get index of entry for a file to be kept
        i = timestamps.index(tsmax)
        j = resubmits.index(resubmax)
        if i != j:
            raise Exception('timestamp/resubmit number conflict for job ') + job

        linenos.pop(i)
        todel += linenos

    todel.sort()

    # if pretend: show indir contents, labeling files to be deleted
    if len(sys.argv) != 2:
        for (i, line) in enumerate(lines):
            if i in todel:
                print(line, '=> del')
            else:
                print(line)

        sys.exit(0)

    # actual deletion of files
    for (i, line) in enumerate(lines):
        if i in todel:
            filename = line.split()[-1]
            command('rm', indir + '/' + filename)

def command(*cmd):
    """Executes EOS command and returns its stdout.

    Also makes sure that the command executed successfully.
    """
    # path to eos executable
    eos = '/afs/cern.ch/project/eos/installation/0.3.4/bin/eos.select'

    # run command
    p = subprocess.Popen([eos] + list(cmd), close_fds=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()

    # check stderr / exit status
    if stderr:
        raise Exception('nonempty stderr:\n' + stderr.strip())
    if p.returncode != 0:
        raise Exception('nonzero exit status')

    return stdout


if __name__ == '__main__':
    main()
