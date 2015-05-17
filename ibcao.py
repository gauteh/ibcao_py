#! /usr/bin/env python
#
# Author: Gaute Hope <gaute.hope@nersc.no> / 2014-02-19
#
# IBCAO helpers

from mpl_toolkits.basemap import Basemap
from pyproj import Proj
import scipy as sc, scipy.io, scipy.interpolate, numpy as np
import matplotlib.cm as cm

import os

class IBCAO:
  """
  A class for setting up a matplotlib.Basemap of the IBCAO. The IBCAO grd
  file can be retrieved from:

    http://www.ngdc.noaa.gov/mgg/bathymetry/arctic/ibcaoversion3.html

  Download file: http://www.ngdc.noaa.gov/mgg/bathymetry/arctic/grids/version3_0/IBCAO_V3_500m_RR.grd

  Specification can be found in file: IBCAO_V3_README.txt from:

    http://www.ngdc.noaa.gov/mgg/bathymetry/arctic/grids/version3_0/

  The specifications are hardcoded into this class, that means that the
  class has to be updated for new versions of the IBCAO.


  The Basemap is set up to use the same projection as the map, UPS (Polar
  Stereographic) with the WGS84 datum. While working in this projection it is
  not necessary to transform the IBCAO image (which for the full version of
  the IBCAO is significant).

  """

  # look in current path for grid file, I usually symlink it in here
  # from somewhere.
  ibcao_grid_name = 'IBCAO_V3_500m_RR.grd'
  ibcao_grid = os.path.join(os.path.dirname(os.path.realpath(__file__)), ibcao_grid_name)

  VERSION = '3.0'
  REFERENCE = 'Jakobsson, M., L. A. Mayer, B. Coakley, J. A. Dowdeswell, S. Forbes, B. Fridman, H. Hodnesdal, R. Noormets, R. Pedersen, M. Rebesco, H.-W. Schenke, Y. Zarayskaya A, D. Accettella, A. Armstrong, R. M. Anderson, P. Bienhoff, A. Camerlenghi, I. Church, M. Edwards, J. V. Gardner, J. K. Hall, B. Hell, O. B. Hestvik, Y. Kristoffersen, C. Marcussen, R. Mohammad, D. Mosher, S. V. Nghiem, M. T. Pedrosa, P. G. Travaglini, and P. Weatherall, The International Bathymetric Chart of the Arctic Ocean (IBCAO) Version 3.0, Geophysical Research Letters, doi: 10.1029/2012GL052219.'

  # previously kept in ibcao.cpt
  COLORMAP = """\
# downloaded from IBCAO homepage
#Discrete color table for Ocean and continous for land in RGB for the Arctic bathymetry and topography
-6000	18	10	59	-5000	18	10	59
-5000	22	44	103	-4000	22	44	103
-4000	22	88	135	-3000	22	88	135
-3000	22	138	170	-2000	22	138	170
-2000	22	154	184	-1500	22	154	184
-1500	23	170	198	-1000	23	170	198
-1000	23	186	212	-500	23	186	212
-500	24	196	223	-250	24	196	223
-250	25	206	234	-100	25	206	234
-100	27	216	245	-75	27	216	245
-75	38	223	241	-50	38	223	241
-50	49	230	236	-25	49	230	236
-25	105	242	233	-10	105	242	233
-10	161	255	230	0	161	255	230
0	40	158	38	25	44	176	42
25	44	176	42	50	49	195	46
50	49	195	46	75	145	208	80
75	145	208	80	100	242	202	90
100	242	202	90	200	227	170	48
200	227	170	48	300	190	140	40
300	190	140	40	400	151	109	31
400	151	109	31	500	114	80	23
500	114	80	23	600	95	63	12
600	95	63	12	700	81	57	16
700	81	57	16	800	114	97	71
800	114	97	71	1000	105	105	105
1000	105	105	105	1500	170	170	170
1500	170	170	170	5000	200	200	200
"""

  def __init__ (self, ibcao_grd_file = ibcao_grid):
    self.ibcao_grid = ibcao_grd_file
    if not os.path.exists (self.ibcao_grid):
      print ('IBCAO grid could not be found in local directory, download from: http://www.ngdc.noaa.gov/mgg/bathymetry/arctic/grids/version3_0/IBCAO_V3_500m_RR.grd')
      raise RuntimeError ('IBCAO grid not found')


    ibcao_nc = scipy.io.netcdf_file (self.ibcao_grid)
    self.ibcao_nc = ibcao_nc

    ## test for version 3
    if not 'ver3.0' in str(ibcao_nc.title):
      raise ValueError ("The IBCAO file specified does not seem to be IBCAO version 3.0")

    # load ibcao projection details
    self.z      = ibcao_nc.variables['z']
    self.ups_x  = ibcao_nc.variables['x']
    self.ups_y  = ibcao_nc.variables['y']

    self.extent     = 2904000 * 2  # from README, northing and easting
    self.dim        = (self.ups_x.shape[0], self.ups_y.shape[0])
    self.resolution = 500 # meters

    self.projection     = 'npstere'
    self.datum          = 'WGS84'
    self.vertical_datum = 'mean sea level'
    self.true_scale     = 75.0  # deg N
    self.scale_factor   = 0.982966757777337
    self.origin_lat     = 90  # deg N
    self.origin_lon     = 0   # deg

    print ("ibcao read, shape:", self.dim)

    # don't close when mmapped: scipy#3630
    #self.ibcao_nc.close ()

    self.basemap = self.get_basemap ()

  def close (self):
    # make sure you don't close in case mmap is used elsewhere
    print ("ibcao: closing map.")
    self.ibcao_nc.close ()

  def get_basemap (self):
    m = Basemap ( projection = self.projection,
                  width      = self.extent,
                  height     = self.extent,
                  lon_0      = self.origin_lon,
                  lat_0      = self.origin_lat,
                  lat_ts     = self.true_scale,
                  k_0        = self.scale_factor,
                  resolution = 'l')

    return m

  def Basemap (self):
    return self.basemap

  depth_f = None
  def get_depth (self, x, y, _order):
    #from mpl_toolkits.basemap import interp

    #return interp (self.z.data.T, self.ups_y.data, self.ups_x.data, y, x, order = _order)

    from scipy.interpolate import interp2d

    if self.depth_f is None:
      print ("setting up interpolation function..")
      self.depth_f = interp2d (self.ups_x.data, self.ups_y.data, self.z.data, fill_value = np.nan)

    return self.depth_f(x-2904000, y-2904000)

  def test_coordintes (self):
    ## test a bunch of coordinates
    print ("IBCAO: test coordinates")

    b = self.Basemap ()

    xin = self.ups_x.data[::10]
    yin = self.ups_y.data[::10]

    xx, yy = np.meshgrid (xin, yin)

    # make lon, lats
    lon, lat = b (xx, yy, inverse = True)

    # do the inverse
    nx, ny = b(lon, lat, inverse = False)

    np.testing.assert_array_almost_equal (xx, nx)
    np.testing.assert_array_almost_equal (yy, ny)




  def Colormap (self):
    # load discrete colormap suggested by official IBCAO
    # loader based on: http://wiki.scipy.org/Cookbook/Matplotlib/Loading_a_colormap_dynamically and
    # http://stackoverflow.com/questions/26559764/matplotlib-pcolormesh-discrete-colors

    cmap = np.empty ((0,4))
    c = 0

    for l in self.COLORMAP.split("\n"):
      l = l.strip()

      if len(l) == 0 or l[0] == '#':
        continue

      ls = np.array([float (v) for v in l.split ()])

      if ls.shape[0] < 8:
        continue

      c += 1
      cmap.resize (c, 4)
      cmap[c-1,:] = ls[:4]

    # add end spec
    c += 1
    cmap.resize (c, 4)
    cmap[c-1,:] = ls[4:]

    # normalize colors
    cmap[:,[1, 2, 3]] = cmap[:,[1, 2, 3]] / 255.

    cmap_out = cm.colors.ListedColormap (cmap[:,1:4], 'ibcao', c)
    norm     = cm.colors.BoundaryNorm (cmap[:,0], c)

    return (cmap_out, norm)


if __name__ == '__main__':
  print ("testing ibcao class")
  import matplotlib.pyplot as plt
  import matplotlib.cm as cm

  plt.figure (1); plt.clf()
  m = IBCAO ()

  m.test_coordintes ()

  b = m.Basemap()

  b.drawcoastlines ()

  # only plot every 'div' data point
  div = 10
  zz = m.z.data[::div, ::div]

  dim = zz.shape[0]
  lons, lats = b.makegrid(dim, dim)
  x, y = b(lons, lats)

  (cmap, norm) = m.Colormap ()
  plt.pcolormesh (x, y, zz, cmap = cmap, norm = norm)

  # set up meridians
  meridians = np.arange (0, 360, 10)
  b.drawmeridians (meridians, labels = [True, True, False, False])

  # parallels
  parallels = np.arange (65, 90, 5)
  b.drawparallels (parallels, labels = [False, False, True, True])

  plt.title ('The International Bathymetric Chart of the Arctic Ocean')
  plt.colorbar ()

  # put labels on the parallels
  for p in parallels:
    x, y = b (0, p)
    plt.text (x, y, str(p))

  x, y = b(0, 90)
  plt.plot (x, y, 'kx')

  ## test depth
  lon = np.linspace (0, 360, 10)
  lat = np.linspace (65, 90, 10)

  #for la in lat:
    #x, y = b(lon, np.repeat(la, len(lon)))
    #plt.plot (x, y, 'rx')

  #plt.figure ()
  lon, lat = np.meshgrid (lon, lat)
  xx, yy = b(lon, lat)
  xx = xx.ravel ()
  yy = yy.ravel ()
  #dz = m.get_depth (xx, yy, 0)

  plt.plot (xx, yy, 'rx')
  for x, y in zip(xx, yy):
    plt.text (x, y, ("%.1f" % m.get_depth(x, y, 0)[0]))


  plt.show (False); plt.draw ()



