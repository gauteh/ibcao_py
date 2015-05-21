import sys
import os.path

import matplotlib
matplotlib.use ('Agg')

sys.path.append ('../')

import unittest as ut

import logging as ll
ll.getLogger().setLevel ('INFO')

TESTDIR = os.path.dirname(__file__) # this script is located in the testdir
outdir  = os.path.join (TESTDIR, 'out')

# check if out dir exists
if not os.path.exists (outdir):
  os.makedirs (outdir)

if os.environ.get ('travis') is not None:
  TRAVIS = True
  ll.info ('running in travis')
else:
  TRAVIS = False

