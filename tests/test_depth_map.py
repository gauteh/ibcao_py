# encoding: utf-8
import common
from common import outdir, TRAVIS
import logging as ll
import unittest as ut

from ibcao  import *
import cartopy.crs as ccrs

import matplotlib
import matplotlib.pyplot as plt

import os
import os.path

class IbcaoDepthTest (ut.TestCase):
  def setUp (self):
    self.i = IBCAO ()

  def tearDown (self):
    self.i.close ()
    del self.i

  def test_resample_depth (self):
    ll.info ('testing resampling of depth')

    div = 100

    (x, y) = self.i.grid

    x = x[::div, ::div]
    y = y[::div, ::div]

    shp = x.shape
    x = x.ravel ()
    y = y.ravel ()

    ll.info ('resampling to: ' + str(shp))

    #z = self.i.interp_depth (x, y)
    z = self.i.map_depth (x, y)
    ll.info ('interpolation done')

    x = x.reshape (shp)
    y = y.reshape (shp)
    z = z.reshape (shp)

    if not TRAVIS:
      # make new map with resampled grid
      plt.figure ()
      ax = plt.axes (projection = self.i.projection)
      ax.set_xlim (*self.i.xlim)
      ax.set_ylim (*self.i.ylim)

      ax.coastlines ('10m')
      # plot every 'div' data point
      (cmap, norm) = self.i.Colormap ()
      cm = ax.pcolormesh (self.i.x[::div], self.i.y[::div], z, cmap = cmap, norm = norm)
      plt.colorbar (cm)

      plt.savefig (os.path.join (outdir, 'resampled_map.png'))



