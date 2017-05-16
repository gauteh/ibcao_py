## IBCAO class reference

## Methods

#### init (ibcao_grd_file = 'IBCAO_V3_500m_RR.grd')

Loads the IBCAO grid, either looks in the current directory for the grid file or it may be specified.

#### template (div = 1)

Returns a matplotlib Figure with the map plotted. `div` specifies how many data points to skip, with 1 meaning plot all data points.

#### grid (div = 1)
Returns a 2D grid in UPS coordinates with desired sampling `div`.

#### Colormap ()
Returns a matplotlib Colormap and Norm tuple.

#### map_depth (x, y, order = 3)

Returns depth at UPS coordinates `x` and `y` using `scipy.ndimage.map_coordinates`.

#### interp_depth (x, y)

Interpolates depth usign `scipy.interpolate.RectBivariateSpline` at UPS coordinates `x` and `y`.

#### get_geod ()
Returns a `pyproj.Geod()` with the `WGS84` ellipsoid.

#### get_proj ()
Returns the correct `pyproj.Proj` for the IBCAO.

#### get_proj_str ()
Returns the `Proj.4` string for the IBCAO UPS variant.

#### get_cartopy ()
Returns the correct set up Cartopy `Stereographic` projection for the IBCAO UPS variant.

## Properties

#### REFERENCE

Holds the citation string for the IBCAO map.

#### COLORMAP
Holds the GMT colormap previously distributed with IBCAO.

#### VERSION
IBCAO version

#### xlim
Extent along longitude (in UPS coordinates, meters)

#### ylim
Extent along latitude (in UPS coordinates, meters)

#### x
Grid points along longitude (UPS coordinates, meters)

#### y
Grid points along latitdude (UPS coordinates, meters)

#### z
Grid of depths at `x` and `y`.





