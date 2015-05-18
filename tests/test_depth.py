import common
import logging as ll
import unittest as ut

from ibcao  import *
import cartopy.crs as ccrs

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
    ll.info ('calculating depth profile along 0E')
    # make a profile along 0E

    lat = np.linspace (60, 90, 1000)
    lon = np.repeat (0, len(lat))

    xy  = self.i.projection.transform_points (ccrs.Geodetic (), lon, lat)

    d = self.i.get_depth (xy[:,0], xy[:,1])

    plt.figure ()
    plt.plot (lat, d)
    plt.title ('depth along 0E')
    plt.xlabel ('Latitude')
    plt.savefig ('out/depth_along_0E.png')

  def test_resample_depth (self):
    ll.info ('testing resampling of depth')

    (x, y) = self.i.grid

    shp = x.shape
    x = x.ravel ()
    y = y.ravel ()

    z = self.i.get_depth (x, y)
    ll.info ('interpolation done')

    x = x.reshape (shp)
    y = y.reshape (shp)
    z = z.reshape (shp)

    # make new map with resampled grid
    plt.figure ()
    ax = plt.axes (projection = self.i.projection)
    ax.set_xlim (*self.i.xlim)
    ax.set_ylim (*self.i.ylim)

    ax.coastlines ('10m')
    # plot every 'div' data point
    (cmap, norm) = self.Colormap ()
    cm = ax.pcolormesh (x[::div], y[::div], z[::div, ::div], cmap = cmap, norm = norm)
    plt.colorbar (cm)

    plt.savefig ('out/resampled_map.png')




