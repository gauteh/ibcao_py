# encoding: utf-8
import common
from common import outdir, TRAVIS
import logging as ll
import unittest as ut

from pyproj import Proj
from ibcao  import *

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

import os
import os.path

class IbcaoProjTest (ut.TestCase):
  def setUp (self):
    self.i = IBCAO ()

  def tearDown (self):
    self.i.close ()
    del self.i

  def get_np_stere (self):
    #np_stere = Proj ("""
      #+proj=stere
      #+lat_ts=%(lat_ts)f
      #+lat_0=%(origin_lat)f
      #+lon_0=%(origin_lon)f
      #+k_0=%(scale_factor)f
      #+x_0=%(x0)f
      #+y_0=%(y0)f
      #""" % {
        #'lat_ts' : self.i.true_scale,
        #'origin_lat' : self.i.origin_lat,
        #'origin_lon' : self.i.origin_lon,
        #'scale_factor' : self.i.scale_factor,
        #'x0' : 0,
        #'y0' : 0
        #})


    return self.i.proj

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


    # from IBCAO v2 Techinical reference
    # https://svn.nersc.no/hycom/browser/MSCPROGS/src/Conf_grid/Code/mod_ibcao.F90?rev=187
    # (probably from IBCAO v2)
    # 26        ! UL -2902500,2902500 (-135, 53:49:1.4687)
    # 27	! UR 2902500, 2902500 (135, 53:49:1.4687)
    # 28	! LL -2902500,-2902500 (-45, 53:49:1.4687)
    # 29	! LR 2902500, -2902500 (45, 53:49:1.4687)

    rtol = 1e7
    eps = 6 # meters
    deps = 0.0001 # degrees

    xy = self.i.projection.transform_point (-135, 53.8166 + 0.00040797, g)
    np.testing.assert_allclose ((-2902500, 2902500), xy, rtol, eps)

    xy = self.i.projection.transform_point (135, 53.8166 + 0.00040797, g)
    np.testing.assert_allclose ((2902500, 2902500), xy, rtol, eps)

    xy = self.i.projection.transform_point (-45, 53.8166 + 0.00040797, g)
    np.testing.assert_allclose ((-2902500, -2902500), xy, rtol, eps)

    xy = self.i.projection.transform_point (45, 53.8166 + 0.00040797, g)
    np.testing.assert_allclose ((2902500, -2902500), xy, rtol, eps)

    # reverse
    dx = g.transform_point (-2902500, 2902500, self.i.projection)
    np.testing.assert_allclose ((-135, 53.8166 + 0.00040797), dx, rtol, deps)

    dx = g.transform_point (2902500, 2902500, self.i.projection)
    np.testing.assert_allclose ((135, 53.8166 + 0.00040797), dx, rtol, deps)

    dx = g.transform_point (-2902500, -2902500, self.i.projection)
    np.testing.assert_allclose ((-45, 53.8166 + 0.00040797), dx, rtol, deps)

    dx = g.transform_point (2902500, -2902500, self.i.projection)
    np.testing.assert_allclose ((45, 53.8166 + 0.00040797), dx, rtol, deps)

    lleft = (self.i.xlim[0], self.i.ylim[0])
    uleft = (self.i.xlim[0], self.i.ylim[1])
    lright = (self.i.xlim[1], self.i.ylim[0])
    uright = (self.i.xlim[1], self.i.ylim[1])

    # latitude calculated using this projection, included for regression testing
    dlleft = (-45, 53.79955358092116)
    duleft = (-135, 53.79955358092116)
    dlright = (45, 53.79955358092116)
    duright = (135, 53.79955358092116)

    # reverse
    dx = g.transform_point (*lleft, src_crs = self.i.projection)
    np.testing.assert_allclose (dlleft, dx, rtol, deps)

    dx = g.transform_point (*uleft, src_crs = self.i.projection)
    np.testing.assert_allclose (duleft, dx, rtol, deps)

    dx = g.transform_point (*lright, src_crs = self.i.projection)
    np.testing.assert_allclose (dlright, dx, rtol, deps)

    dx = g.transform_point (*uright, src_crs = self.i.projection)
    np.testing.assert_allclose (duright, dx, rtol, deps)

    # forward
    xy = self.i.projection.transform_point (*dlleft, src_crs = g)
    np.testing.assert_allclose (lleft, xy, rtol, eps)

    xy = self.i.projection.transform_point (*duleft, src_crs = g)
    np.testing.assert_allclose (uleft, xy, rtol, eps)

    xy = self.i.projection.transform_point (*dlright, src_crs = g)
    np.testing.assert_allclose (lright, xy, rtol, eps)

    xy = self.i.projection.transform_point (*duright, src_crs = g)
    np.testing.assert_allclose (uright, xy, rtol, eps)

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

    x = xy[:,0]
    y = xy[:,1]

    nx, ny = np_stere (llon, llat)

    np.testing.assert_allclose (x, nx )
    np.testing.assert_allclose (y, ny )


