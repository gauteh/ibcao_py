import common
import logging as ll
import unittest as ut

from ibcao  import *

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use ('Agg')

import os
import os.path

class IbcaoPlotTest (ut.TestCase):
  def setUp (self):
    self.i = IBCAO ()
    if not os.path.exists ('out'):
      os.makedirs ('out')

  def tearDown (self):
    self.i.close ()
    del self.i

  def test_depths (self):
    pass

