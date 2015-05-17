import sys
import os.path

sys.path.append ('../')

import unittest as ut

import logging as ll
ll.getLogger().setLevel ('INFO')

TESTDIR = os.path.dirname(__file__) # this script is located in the testdir

