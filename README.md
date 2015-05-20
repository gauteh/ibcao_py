# IBCAO py
[![Build Status](https://travis-ci.org/gauteh/ibcao_py.svg?branch=master)](https://travis-ci.org/gauteh/ibcao_py)

Class which sets up the [IBCAO](http://www.ngdc.noaa.gov/mgg/bathymetry/arctic/arctic.html) (projection and loads file) for use with Matplotlib.

> The IBCAO is provided by: <br />
> <br />
> Jakobsson, M., L. A. Mayer, B. Coakley, J. A. Dowdeswell, S. Forbes, B. Fridman, H. Hodnesdal, R. Noormets, R. Pedersen, M. Rebesco, H.-W. Schenke, Y. Zarayskaya A, D. Accettella, A. Armstrong, R. M. Anderson, P. Bienhoff, A. Camerlenghi, I. Church, M. Edwards, J. V. Gardner, J. K. Hall, B. Hell, O. B. Hestvik, Y. Kristoffersen, C. Marcussen, R. Mohammad, D. Mosher, S. V. Nghiem, M. T. Pedrosa, P. G. Travaglini, and P. Weatherall, The International Bathymetric Chart of the Arctic Ocean (IBCAO) Version 3.0, Geophysical Research Letters, doi: 10.1029/2012GL052219.

<img src="ibcao_example.png" />

## Usage

Download the IBCAO grid: [ngdc.noaa.gov](http://www.ngdc.noaa.gov/mgg/bathymetry/arctic/grids/version3_0/IBCAO_V3_500m_RR.grd)

Run test with:
```sh
$ python ibcao.py
```

or in your code do something like:
```python
  print ("testing ibcao class")
  import matplotlib.pyplot as plt
  import matplotlib.cm as cm

  i = IBCAO ()

  f = i.template (10) # only plot every 10th data point

  # lets put some text along the parallels
  lat = np.arange (65, 90, 5)
  lon = np.repeat (0, len(lat))

  # regular lat, lon projection
  g = ccrs.Geodetic ()

  for lon, lat in zip (lon, lat):
    plt.text (lon, lat, str(lat), transform = g)

  # and some along the meridians
  lon = [-45, 45, 135, -135]
  lat = np.repeat (70, len(lon))

  for lon, lat in zip (lon, lat):
    plt.text (lon, lat, str(lon), transform = g)

  # also; the north pole
  plt.text (0, 90, "NP", transform = g)

  plt.show ()
```

## Licence / Copyright / Attribution

Author: Gaute Hope / gaute.hope@nersc.no

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

