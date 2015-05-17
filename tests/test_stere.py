import common
import logging as ll
import unittest as ut

from pyproj import Proj
from ibcao  import *

import matplotlib.pyplot as plt

import os
import os.path

class StereTest (ut.TestCase):
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
        'x0' : 2904000,
        'y0' : 2904000
        })


    return np_stere


  def test_np_stere (self):
    ll.info ("testing np stereographic vs ups")
    np_stere = self.get_np_stere ()

    #b = self.i.basemap

    lon = np.arange (0, 180, 1)
    lat = np.arange (60, 90, 1)

    llon, llat = np.meshgrid (lon, lat)
    llon = llon.ravel ()
    llat = llat.ravel ()

    #x, y = b (llon, llat)

    nx, ny = np_stere (llon, llat)

    #np.testing.assert_array_equal (x, nx )



  def test_ups (self):
    ups = Proj ("""
      +proj=ups
      +north
      """)

  def test_ups_vs_np_stere (self):
    pass

  def test_make_test_map (self):
    plt.figure ()

    ax = plt.axes (projection = self.i.projection)
    #ax.set_extents (-self.i.extent, self.i.extent, -self.i.extent, self.i.extent)
    ax.coastlines ('10m')
    ax.gridlines ()

    # only plot every 'div' data point
    div = 10
    zz = self.i.z.data[::div, ::div]

    dim = zz.shape[0]
    #lons, lats = b.makegrid(dim, dim)
    #x, y = b(lons, lats)

    x = np.linspace (-2904000, 2904000, dim)
    y = np.linspace (-2904000, 2904000, dim)

    (cmap, norm) = self.i.Colormap ()
    cm = ax.pcolormesh (x, y, zz, cmap = cmap, norm = norm)
    plt.colorbar (cm)

    ## set up meridians
    #meridians = np.arange (0, 360, 10)
    #b.drawmeridians (meridians, labels = [True, True, False, False])

    ## parallels
    #parallels = np.arange (65, 90, 5)
    #b.drawparallels (parallels, labels = [False, False, True, True])

    plt.title ('The International Bathymetric Chart of the Arctic Ocean')


    plt.savefig ('out/test.png')

  def test_coordintes (self):
    ## test a bunch of coordinates
    print ("IBCAO: test coordinates")

    #b = self.Basemap ()

    #xin = self.ups_x.data[::10]
    #yin = self.ups_y.data[::10]

    #xx, yy = np.meshgrid (xin, yin)

    ## make lon, lats
    #lon, lat = b (xx, yy, inverse = True)

    ## do the inverse
    #nx, ny = b(lon, lat, inverse = False)

    #np.testing.assert_array_almost_equal (xx, nx)
    #np.testing.assert_array_almost_equal (yy, ny)



