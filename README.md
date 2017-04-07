# IBCAO py
Class which sets up the [IBCAO](http://www.ngdc.noaa.gov/mgg/bathymetry/arctic/arctic.html) (projection and loads file) for use with [Matplotlib](http://matplotlib.org/) and [Cartopy](http://scitools.org.uk/cartopy/).

<img src="ibcao_example.png" />

## Usage

Download the IBCAO grid: [ngdc.noaa.gov](http://www.ngdc.noaa.gov/mgg/bathymetry/arctic/grids/version3_0/IBCAO_V3_500m_RR.grd.gz)

Run test with:
```sh
$ python ibcao.py
```

or in your code do something like:
```python
  print ("testing ibcao class")
  import matplotlib.pyplot as plt
  import matplotlib.cm as cm
  import cartopy.crs as ccrs
  from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

  i = IBCAO ()

  f = i.template ()

  # lets put some text along the parallels
  lat = np.arange (65, 90, 5)
  lon = np.repeat (0, len(lat))

  # regular lat, lon projection
  g = ccrs.Geodetic ()

  for lon, lat in zip (lon, lat):
    plt.text (lon, lat, LATITUDE_FORMATTER.format_data(lat), transform = g)

  # and some along the meridians
  lon = [-45, 45, 135, -135]
  lat = np.repeat (70, len(lon))

  for lon, lat in zip (lon, lat):
    plt.text (lon, lat, LONGITUDE_FORMATTER.format_data(lon), transform = g)

  # also; the north pole
  plt.text (0, 90, "NP", transform = g)

  plt.show ()
```

check out the test cases in `tests/` for some inspiration on how to use the
class.

## Reference

> The IBCAO is provided by: <br />
> <br />
> Jakobsson, M., L. A. Mayer, B. Coakley, J. A. Dowdeswell, S. Forbes, B. Fridman, H. Hodnesdal, R. Noormets, R. Pedersen, M. Rebesco, H.-W. Schenke, Y. Zarayskaya A, D. Accettella, A. Armstrong, R. M. Anderson, P. Bienhoff, A. Camerlenghi, I. Church, M. Edwards, J. V. Gardner, J. K. Hall, B. Hell, O. B. Hestvik, Y. Kristoffersen, C. Marcussen, R. Mohammad, D. Mosher, S. V. Nghiem, M. T. Pedrosa, P. G. Travaglini, and P. Weatherall, The International Bathymetric Chart of the Arctic Ocean (IBCAO) Version 3.0, Geophysical Research Letters, doi: 10.1029/2012GL052219.


## Licence / Copyright / Attribution

Author: Gaute Hope / gaute.hope@nersc.no

This work is licenced under the GNU Lesser General Public Licence (LGPLv3).

