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
  ibcao_grid = '/home/gaute/ymse/maps/IBCAO-3rd-Edition/IBCAO_Ver3_RR_2012-03-16.grd'
  ibcao_cpt  = os.path.join (os.path.dirname(os.path.realpath(__file__)), 'ibcao.cpt')

  VERSION = '3.0'
  REFERENCE = 'Jakobsson, M., L. A. Mayer, B. Coakley, J. A. Dowdeswell, S. Forbes, B. Fridman, H. Hodnesdal, R. Noormets, R. Pedersen, M. Rebesco, H.-W. Schenke, Y. Zarayskaya A, D. Accettella, A. Armstrong, R. M. Anderson, P. Bienhoff, A. Camerlenghi, I. Church, M. Edwards, J. V. Gardner, J. K. Hall, B. Hell, O. B. Hestvik, Y. Kristoffersen, C. Marcussen, R. Mohammad, D. Mosher, S. V. Nghiem, M. T. Pedrosa, P. G. Travaglini, and P. Weatherall, The International Bathymetric Chart of the Arctic Ocean (IBCAO) Version 3.0, Geophysical Research Letters, doi: 10.1029/2012GL052219.'

  def __init__ (self, ibcao_grd_file = ibcao_grid):
    self.ibcao_grid = ibcao_grd_file
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

    self.projection     = 'stere'
    self.datum          = 'WGS84'
    self.vertical_datum = 'mean sea level'
    self.true_scale     = 75.0  # deg N
    self.scale_factor   = 0.982966757777337
    self.origin_lat     = 90  # deg N
    self.origin_lon     = 0   # deg

    print ("ibcao read, shape:", self.dim)
    #self.ibcao_nc.close ()

  def Basemap (self):
    m = Basemap ( projection = self.projection,
                  width      = self.extent,
                  height     = self.extent,
                  lon_0      = self.origin_lon,
                  lat_0      = self.origin_lat,
                  lat_ts     = self.true_scale,
                  k_0        = self.scale_factor,
                  resolution = 'l')

    return m

  def get_depth (self, x, y):
    # input is UPS coordinates
    mxx = self.ups_x.data
    myy = self.ups_y.data
    z   = self.z.data

    from scipy.ndimage import map_coordinates

    print ("ibcao: interpolating..")

    # array/image coordinates
    xx = np.interp (x, mxx, np.arange(0, len(mxx)))
    yy = np.interp (y, myy, np.arange(0, len(myy)))


    return sc.interpolate.griddata ((mx.ravel(), my.ravel()), z.ravel(), (xx, yy), method = 'nearest')


  def Colormap (self):
    # load discrete colormap suggested by official IBCAO
    # loader based on: http://wiki.scipy.org/Cookbook/Matplotlib/Loading_a_colormap_dynamically

    with open (self.ibcao_cpt, 'r') as fd:
      lines = fd.readlines ()

    cmap = np.empty ((0,4))
    c = 0

    lastgood = None

    for l in lines:
      if l[0] == '#':
        continue
      ls = np.array([float (v) for v in l.split ()])

      if ls.shape[0] < 8:
        continue

      c += 1
      cmap.resize (c, 4)
      cmap[c-1,:] = ls[:4] # skip end spec from cpt
      lastgood    = ls

    # add last end spec from cpt
    c+= 1
    cmap.resize (c, 4)
    cmap[c-1,:] = lastgood[4:]

    cmap[:,[1, 2, 3]] = cmap[:,[1, 2, 3]] / 255.

    xn = cmap[:,0]
    xn = (xn - xn[0])/(xn[-1] - xn[0])
    cmap[:,0] = xn

    cmap_dict = { "red"   : list(cmap[:,[0, 1, 1]]),
                  "green" : list(cmap[:,[0, 2, 2]]),
                  "blue"  : list(cmap[:,[0, 3, 3]])
                 }

    cmap_out = cm.colors.LinearSegmentedColormap('ibcao',
               cmap_dict)

    return cmap_out



if __name__ == '__main__':
  print ("test ibcao class")
  import matplotlib.pyplot as plt
  import matplotlib.cm as cm

  m = IBCAO ()
  b = m.Basemap()

  b.drawcoastlines ()

  # only plot every 'div' data point
  div = 10
  zz = m.z.data[::div, ::div]

  dim = zz.shape[0]
  lons, lats = b.makegrid(dim, dim)
  x, y = b(lons, lats)

  cmap = m.Colormap ()
  plt.pcolormesh (x, y, zz)

  # set up meridians
  meridians = np.arange (0, 360, 10)
  b.drawmeridians (meridians, labels = [True, True, False, False])

  # parallels
  parallels = np.arange (70, 90, 5)
  b.drawparallels (parallels, labels = [False, False, True, True])

  plt.title ('The International Bathymetric Chart of the Arctic Ocean')

  plt.show ()

