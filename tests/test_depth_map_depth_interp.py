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

  def get_lon_lat (self, nlat = 100, nlon = 100):
    lat = np.linspace (60, 90, nlat)
    lon = np.linspace (-180, 180, nlon)

    lat, lon = np.meshgrid (lat, lon)
    lat = lat.ravel ()
    lon = lon.ravel ()

    return (lon, lat)

  def test_map_depth_vs_interp_depth (self):
    ll.info ('testing map_depth vs interp_depth')
    # make a profile

    if TRAVIS:
      lon, lat = self.get_lon_lat (30, 30)
    else:
      lon, lat = self.get_lon_lat ()

    xy  = self.i.projection.transform_points (ccrs.Geodetic (), lon, lat)

    x = xy[:,0]
    y = xy[:,1]

    md = self.i.map_depth (x, y)

    id = self.i.interp_depth (x, y)

    if not TRAVIS:
      plt.figure ()
      plt.plot (lat, md, label = 'map_depth')
      plt.plot (lat, id, label = 'interp_depth')
      plt.legend ()
      plt.title ('depth')
      plt.xlabel ('Latitude')
      plt.savefig (os.path.join (outdir, 'depth_map_depth_vs_interp_depth.png'))

    np.testing.assert_allclose (md, id, atol = 1)


