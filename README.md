# IBCAO py

Class which sets up the IBCAO (projection and loads file) for use with Matplotlib.

<img src="http://scipy-central.org/media/scipy_central/images/201403/ibcao.png" />

## Usage

Run test with:
```sh
$ python ibcao.py
```

or in your code do something like:
```python
  print ("testing ibcao class")
  from ibcao import *
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
  plt.pcolormesh (x, y, zz, cmap = cmap)

  # set up meridians
  meridians = np.arange (0, 360, 10)
  b.drawmeridians (meridians, labels = [True, True, False, False])

  # parallels
  parallels = np.arange (70, 90, 5)
  b.drawparallels (parallels, labels = [False, False, True, True])

  plt.title ('The International Bathymetric Chart of the Arctic Ocean')

  plt.show ()
```

## Licence / Copyright / Attribution

Author: Gaute Hope / gaute.hope@nersc.no

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

