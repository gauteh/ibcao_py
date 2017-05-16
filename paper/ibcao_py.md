  ---
  title: 'IBCAO_py: A matplotlib library for using the International Bathymetric Chart of the Arctic Ocean with cartopy and matplotlib'
  tags:
    - ibcao
    - matplotlib
    - cartopy
    - python
    - gis
    - map
    - arctic
  authors:
   - name: Gaute Hope
     orcid: 0000-0002-5653-1447
     affiliation: 1
  affiliations:
   - name: Nansen Environmental and Remote Sensing Center
     index: 1
  date: 04 April 2017
  bibliography: ibcao_py.bib
  ---

  # Summary

  This is a python plotting toolbox for using the International Bathymetric
  Chart of the Arctic Ocean [@Jakobsson2012] with Cartopy [@Cartopy] in
  matplotlib [@matplotlib] suitable for scientist creating figures for
  publications, automated visualization of data, and querying the depth of the
  Arctic ocean either for single use or in an automatic fashion.

  The [IBCAO](http://www.ngdc.noaa.gov/mgg/bathymetry/arctic/arctic.html) is
  distributed using the Universal Polar Stereographic projection (UPS) with custom
  parameters and grid-spacing. This package sets up the projection correctly, and
  loads the map data in an efficient way. This ensures that no transformation is
  needed when plotting the map, and that data that is plotted on the map is
  correctly positioned. A ready figure with the map loaded is provided, with a
  plotting transformation to the Geodetic projection ready so that data provided
  in the familiar latitude and longitude coordinates may be plotted easily.

  Additionally, efficient interpolation routines for reading the bathymetry
  (depth) from the map data at coordinates, tracks or grids of coordinates are
  provided so that these may be easily read.

  The class may it self be used as demonstration, though plotting the IBCAO is
  a matter of four lines of python code. The documentation showcases plotting
  of the IBCAO, plotting of data on top of the map and retrieval of a depth
  profile. The package is covered by a test suite.


  -![IBCAO plotted with ibcao_py](ibcao_example.png)

  # References

