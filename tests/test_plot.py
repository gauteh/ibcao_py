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

  def test_template (self):
    ll.info ("testing template")
    f = self.i.template (10)

    f.savefig ('out/test_template.png')

  def test_make_test_map (self):
    ll.info ("make test map")
    plt.figure ()

    ax = plt.axes (projection = self.i.projection)
    #ax.set_extent ([-self.i.extent, self.i.extent, -self.i.extent, self.i.extent])
    ax.set_xlim ([-self.i.extent, self.i.extent])
    ax.set_ylim ([-self.i.extent, self.i.extent])
    ax.coastlines ('10m')
    ax.gridlines ()

    # only plot every 'div' data point
    div = 10
    zz = self.i.z[::div, ::div]

    dim = zz.shape[0]

    x = np.linspace (-2904000, 2904000, dim)
    y = np.linspace (-2904000, 2904000, dim)

    (cmap, norm) = self.i.Colormap ()
    cm = ax.pcolormesh (self.i.x[::div], self.i.y[::div], zz, cmap = cmap, norm = norm)
    plt.colorbar (cm)

    plt.title ('The International Bathymetric Chart of the Arctic Ocean')

    plt.savefig ('out/test.png')

