import common
from common import outdir
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

  def test_depths (self):
    ll.info ('calculating depth profile along 0E')
    # make a profile along 0E

    lat = np.linspace (60, 90, 1000)
    lon = np.repeat (0, len(lat))

    xy  = self.i.projection.transform_points (ccrs.Geodetic (), lon, lat)

    d = self.i.interp_depth (xy[:,0], xy[:,1])
    ll.info ('d=')
    ll.info (d.shape)

    plt.figure ()
    plt.plot (lat, d)
    plt.title ('depth along 0E')
    plt.xlabel ('Latitude')
    plt.savefig (os.path.join(outdir, 'depth_along_0E.png'))

  def test_map_coordinates (self):
    ll.info ('testing map coordinates')
    # make a profile along 0E

    lat = np.linspace (60, 90, 1000)
    lon = np.repeat (0, len(lat))

    xy  = self.i.projection.transform_points (ccrs.Geodetic (), lon, lat)

    from scipy.ndimage import map_coordinates

    x = (xy[:,0] + 2904000 ) / 500
    y = (xy[:,1] + 2904000 ) / 500

    z = map_coordinates (self.i.z.T, [x, y], cval = np.nan)

    dz = self.i.interp_depth (xy[:,0], xy[:,1])
    ll.info ('dz=')
    ll.info (dz.shape)

    plt.figure ()
    plt.plot (lat, z, label = 'map_coordinates')
    plt.plot (lat, dz, label = 'default')
    plt.legend ()
    plt.title ('depth along 0E')
    plt.xlabel ('Latitude')
    plt.savefig (os.path.join (outdir, 'depth_along_0E_map_coordinates.png'))

    np.testing.assert_allclose (dz, z, atol = 1)

  def test_interp2d (self):
    ll.info ('testing vs interp2d')

    lat = np.linspace (60, 90, 1000)
    lon = np.repeat (0, len(lat))

    xy  = self.i.projection.transform_points (ccrs.Geodetic (), lon, lat)

    from scipy.interpolate import interp2d
    depth_f = interp2d (self.i.x, self.i.y, self.i.z, fill_value = np.nan, kind = 'cubic')

    d = depth_f (xy[:,0], xy[:,1])
    dz = self.i.interp_depth (xy[:,0], xy[:,1])

    d = d.diagonal ()

    plt.figure ()
    plt.plot (lat, d, label = 'interp2d')
    plt.plot (lat, dz, label = 'default')
    plt.legend ()
    plt.title ('depth along 0E')
    plt.xlabel ('Latitude')
    plt.savefig (os.path.join (outdir, 'depth_along_0E_interp2d.png'))

    np.testing.assert_allclose (dz, d, atol = 10)

  def test_rect_bivariate_spline (self):
    ll.info ('testing rectbivariatespline')
    from scipy.interpolate import RectBivariateSpline

    lat = np.linspace (60, 90, 1000)
    lon = np.repeat (0, len(lat))

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

    dz = self.i.interp_depth (xy[:,0], xy[:,1])

    plt.figure ()
    plt.plot (lat, d, label = 'rectbivariatespline')
    plt.plot (lat, dz, label = 'default')
    plt.legend ()
    plt.title ('depth along 0E rectbivariate')
    plt.xlabel ('Latitude')
    plt.savefig (os.path.join (outdir, 'depth_along_0E_rectbivariate.png'))

    np.testing.assert_allclose (dz, d, atol = 1)


  def test_known_positions (self):
    ll.info ('testing depth on a few known positions')

    g = ccrs.Geodetic ()

    def check_pos (lon, lat, depth, _atol = 0.1, _rtol = 1e-7):
      xy = self.i.projection.transform_point(lon, lat, g)

      d = self.i.interp_depth (np.array([xy[0]]), np.array([xy[1]]))
      np.testing.assert_allclose (d, depth, atol = _atol, rtol = _rtol)


    # north pole
    check_pos (0, 90, -4261, 50)

    # longyearbyen
    check_pos (15.651140, 78.222665, 1.7, 7)

    # highest mountain on greenland (Gunnbjørn Fjeld)
    check_pos (-29.898533, 68.9195, 3694, 400)


  def test_resample_depth (self):
    ll.info ('testing resampling of depth')

    (x, y) = self.i.grid

    shp = x.shape
    x = x.ravel ()
    y = y.ravel ()

    #z = self.i.interp_depth (x, y)
    z = self.i.map_depth (x, y)
    ll.info ('interpolation done')

    x = x.reshape (shp)
    y = y.reshape (shp)
    z = z.reshape (shp)

    div = 10

    # make new map with resampled grid
    plt.figure ()
    ax = plt.axes (projection = self.i.projection)
    ax.set_xlim (*self.i.xlim)
    ax.set_ylim (*self.i.ylim)

    ax.coastlines ('10m')
    # plot every 'div' data point
    (cmap, norm) = self.i.Colormap ()
    cm = ax.pcolormesh (self.i.x[::div], self.i.y[::div], z[::div, ::div], cmap = cmap, norm = norm)
    plt.colorbar (cm)

    plt.savefig (os.path.join (outdir, 'resampled_map.png'))



