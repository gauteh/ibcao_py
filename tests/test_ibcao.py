import common
import logging as ll
import unittest as ut

from pyproj import Proj
from ibcao  import *

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

import os
import os.path

class IbcaoTest (ut.TestCase):
  def setUp (self):
    self.i = IBCAO ()
    if not os.path.exists ('out'):
      os.makedirs ('out')

  def tearDown (self):
    self.i.close ()
    del self.i

  def get_np_stere (self):
    np_stere = Proj ("""
      +proj=stere
      +lat_ts=%(lat_ts)f
      +lat_0=%(origin_lat)f
      +lon_0=%(origin_lon)f
      +k_0=%(scale_factor)f
      +x_0=%(x0)f
      +y_0=%(y0)f
      """ % {
        'lat_ts' : self.i.true_scale,
        'origin_lat' : self.i.origin_lat,
        'origin_lon' : self.i.origin_lon,
        'scale_factor' : self.i.scale_factor,
        'x0' : 0,
        'y0' : 0
        })


    return np_stere

  def test_ibcao_grid (self):
    ll.info ('test grid coordinates')

    xin = self.i.x[::10]
    yin = self.i.y[::10]

    xx, yy = np.meshgrid (xin, yin)
    xx = xx.ravel ()
    yy = yy.ravel ()

    ## make lon, lats
    g = ccrs.Geodetic ()
    gxy = g.transform_points (self.i.projection, xx, yy)

    ## do the inverse
    xy = self.i.projection.transform_points (g, gxy[:,0], gxy[:,1])

    np.testing.assert_array_almost_equal (xx, xy[:,0])
    np.testing.assert_array_almost_equal (yy, xy[:,1])

  def test_north_pole (self):
    ll.info ('test north pole')

    g = ccrs.Geodetic ()

    # north pole
    lon = np.arange (-180, 180, 1)
    lat = np.repeat (90, len(lon))

    nx = self.i.projection.transform_points (g, lon, lat)

    np.testing.assert_array_equal (nx[:,0:2], np.zeros ((nx.shape[0], 2)))

    # test inverse conversion
    lx = g.transform_points (self.i.projection, nx[:,0], nx[:,1])
    #np.testing.assert_array_equal (lon, lx[:,0]) # not unique
    np.testing.assert_array_equal (lat, lx[:,1])

  def test_corners (self):
    ll.info ('test corners')

    g = ccrs.Geodetic ()

    lleft = (self.i.xlim[0], self.i.ylim[0])
    uleft = (self.i.xlim[0], self.i.ylim[1])
    lright = (self.i.xlim[1], self.i.ylim[0])
    uright = (self.i.xlim[1], self.i.ylim[1])

    # probably from IBCAO v2
    # https://svn.nersc.no/hycom/browser/MSCPROGS/src/Conf_grid/Code/mod_ibcao.F90?rev=187
    # 26        ! UL -2902500,2902500 (-135, 53:49:1.4687)
    # 27	! UR 2902500, 2902500 (135, 53:49:1.4687)
    # 28	! LL -2902500,-2902500 (-45, 53:49:1.4687)
    # 29	! LR 2902500, -2902500 (45, 53:49:1.4687)

    eps = 6 # meters

    xy = self.i.projection.transform_point (-135, 53.8166 + 0.00040797, g)
    np.testing.assert_allclose ((-2902500, 2902500), xy, eps, eps)

    xy = self.i.projection.transform_point (135, 53.8166 + 0.00040797, g)
    np.testing.assert_allclose ((2902500, 2902500), xy, eps, eps)

    xy = self.i.projection.transform_point (-45, 53.8166 + 0.00040797, g)
    np.testing.assert_allclose ((-2902500, -2902500), xy, eps, eps)

    xy = self.i.projection.transform_point (45, 53.8166 + 0.00040797, g)
    np.testing.assert_allclose ((2902500, -2902500), xy, eps, eps)


  def test_np_stere (self):
    ll.info ("testing np stereographic vs our projection")
    np_stere = self.get_np_stere ()

    lon = np.arange (-180, 180, 1)
    lat = np.arange (80, 90, 1)

    llon, llat = np.meshgrid (lon, lat)
    llon = llon.ravel ()
    llat = llat.ravel ()

    # convert to np_stere
    geodetic = ccrs.Geodetic ()
    xy = self.i.projection.transform_points (geodetic, llon, llat)
    print (xy)

    x = xy[:,0]
    y = xy[:,1]

    nx, ny = np_stere (llon, llat)

    np.testing.assert_array_equal (x, nx )
    np.testing.assert_array_equal (y, ny )

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
    #lons, lats = b.makegrid(dim, dim)
    #x, y = b(lons, lats)

    x = np.linspace (-2904000, 2904000, dim)
    y = np.linspace (-2904000, 2904000, dim)

    (cmap, norm) = self.i.Colormap ()
    cm = ax.pcolormesh (self.i.x[::div], self.i.y[::div], zz, cmap = cmap, norm = norm)
    plt.colorbar (cm)

    ## set up meridians
    #meridians = np.arange (0, 360, 10)
    #b.drawmeridians (meridians, labels = [True, True, False, False])

    ## parallels
    #parallels = np.arange (65, 90, 5)
    #b.drawparallels (parallels, labels = [False, False, True, True])

    plt.title ('The International Bathymetric Chart of the Arctic Ocean')


    plt.savefig ('out/test.png')



