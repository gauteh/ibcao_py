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

  def test_map_coordinates (self):
    ll.info ('testing map coordinates')
    # make a profile

    lon, lat = self.get_lon_lat (nlat = 100, nlon = 100)

    xy  = self.i.projection.transform_points (ccrs.Geodetic (), lon, lat)

    from scipy.ndimage import map_coordinates

    x = (xy[:,0] + 2904000 ) / 500
    y = (xy[:,1] + 2904000 ) / 500

    z = map_coordinates (self.i.z.T, [x, y], cval = np.nan)

    dz = self.i.interp_depth (xy[:,0], xy[:,1])
    ll.info ('dz=')
    ll.info (dz.shape)

    if not TRAVIS:
      plt.figure ()
      plt.plot (lat, z, label = 'map_coordinates')
      plt.plot (lat, dz, label = 'default')
      plt.legend ()
      plt.title ('depth')
      plt.xlabel ('Latitude')
      plt.savefig (os.path.join (outdir, 'depth_map_coordinates.png'))

    np.testing.assert_allclose (dz, z, atol = 1)

  def test_rect_bivariate_spline (self):
    ll.info ('testing rectbivariatespline')
    from scipy.interpolate import RectBivariateSpline

    lon, lat = self.get_lon_lat ()

    xy  = self.i.projection.transform_points (ccrs.Geodetic (), lon, lat)

    depth_f = RectBivariateSpline (self.i.x, self.i.y, self.i.z.T)

    d = depth_f.ev(xy[:,0], xy[:,1])

    x = xy[:,0]
    y = xy[:,1]

    # catch outliers
    d[x<self.i.xlim[0]] = np.nan
    d[x>self.i.xlim[1]] = np.nan
    d[y<self.i.ylim[0]] = np.nan
    d[y>self.i.ylim[1]] = np.nan

    ll.info ('running interp_depth..')

    dz = self.i.interp_depth (xy[:,0], xy[:,1])

    if not TRAVIS:
      plt.figure ()
      plt.plot (lat, d, label = 'rectbivariatespline')
      plt.plot (lat, dz, label = 'default')
      plt.legend ()
      plt.title ('depth rectbivariate')
      plt.xlabel ('Latitude')
      plt.savefig (os.path.join (outdir, 'depth_rectbivariate.png'))

    np.testing.assert_allclose (dz, d, atol = 1)

  def test_map_depth_vs_interp_depth (self):
    ll.info ('testing map_depth vs interp_depth')
    # make a profile

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


