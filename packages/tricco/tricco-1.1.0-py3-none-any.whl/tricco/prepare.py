import numpy as np
import xarray as xr


def prepare_grid(model, path, file):
    """
    Returns grid as xarray dataset.
    
    We only need the following information about the horizontal triangular grid:
        - the edge neighbors of a given triangle
        - the three edges of a given triangle
        - the two vertices of a given edge 
    
        Input:
            model string      name of considered model
            path  string      location where gridfile is stored
            file  string      name of the file containing the grid

        Output:
            grid as xarray dataset
    """
    if model == 'ICON':
        _ds_grid = _grid_icon(path+file)
    return _ds_grid


# implementation for ICON model
def _grid_icon(_gridfile):
    
    ds_grid = xr.open_dataset(_gridfile)
    ds_grid = ds_grid[['neighbor_cell_index', 'edge_of_cell', 'edge_vertices']]
    
    # in the ICON model grid, the indexing of the triangle cells and vertices 
    # starts with 1 and not with 0 as assumed by tricco --> we need to subtract 1 here
    ds_grid['neighbor_cell_index'] = ds_grid['neighbor_cell_index'] - 1
    ds_grid['edge_of_cell'] = ds_grid['edge_of_cell'] - 1
    ds_grid['edge_vertices'] = ds_grid['edge_vertices'] - 1
    
    # after the substraction of 1, triangles at the grid border claim to be adjacent to -1
    # --> we set these values to -9999 to clearly flag that there is no neighboing triangle
    #     note: the -9999 value as a flag is used in the function "cubing_next_round"
    ds_grid['neighbor_cell_index'] = xr.where(ds_grid['neighbor_cell_index']!=-1, ds_grid['neighbor_cell_index'], -9999)
    
    return ds_grid


def prepare_field(model, path, file, var, threshold, cubulation):
    """
    Returns one-level data field as a numpy array, also applies threshold-based mask.
    
        Input:
            model     : name of considered model
            path      : path to file
            file      : file containing the data field
            var       : variabe name
            threshold : set field to one if field>=threshold, and to zero otherwise
            cubulation: cubulation of horizontal grid

        Output:
            field both on the triangular grid as well as on the cubulated grid
    """
    if model == 'ICON':
        _field, _field_cube = _field_icon(path, file, var, threshold, cubulation)
    return _field, _field_cube


def prepare_field_lev(model, path, file, var, threshold, cubulation):
    """
    Returns many-level data field as a numpy array, also applies threshold-based mask.
    
        Input:
            model     : name of considered model
            path      : path to file
            file      : file containing the data field
            var       : variabe name
            threshold : set field to one if field>=threshold, and to zero otherwise
            cubulation: cubulation of horizontal grid
            
        Output:
            field both on the triangular grid as well as on the cubulated grid
    """
    if model == 'ICON':
        _field, _field_cube = _field_icon_lev(path, file, var, threshold, cubulation)
    return _field, _field_cube

def prepare_field_ilev(model, path, file, var, threshold, cubulation, ilev):
    """
    Returns a single level of many-level data field as a numpy array, also applies threshold-based mask.
    
        Input:
            model     : name of considered model
            path      : path to file
            file      : file containing the data field
            var       : variabe name
            threshold : set field to one if field>=threshold, and to zero otherwise
            cubulation: cubulation of horizontal grid
            ilev      : index of the level that should be returned
            
        Output:
            field both on the triangular grid as well as on the cubulated grid
    """
    if model == 'ICON':
        _field, _field_cube = _field_icon_ilev(path, file, var, threshold, cubulation, ilev)
    return _field, _field_cube


#------------------------------
# implementation for ICON model
#------------------------------

def _field_icon(path, file, var, threshold, cubulation):
    """"
    Return thresholded 2d data and its cubulated version.
    """
    # field on triangular grid
    field = xr.open_dataset(path + file)[var].squeeze().values
    # threshold field
    field = np.where(field<threshold, 0, 1)
    
    # determine size of array that holds cubulation
    array_size=0
    for ind in [0,1,2]:
        xlist=list()
        for entry in cubulation:
            xlist.append(entry[1][ind])
        array_size=max(array_size, max(xlist))
    array_size=array_size+1 # need to add one as cubulation indices start with 1 instead of 0
    # map field from triangular grid to field on cubic grid
    field_cube = np.zeros((array_size, array_size, array_size), dtype = 'byte')
    for entry in cubulation:
        triangle = entry[0]     # index of triangle
        cube = entry[1]         # cube coordinate
        field_cube[cube[0], cube[1], cube[2]] = field[triangle]

    return field, field_cube

# data on multiple levels
def _field_icon_lev(path, file, var, threshold, cubulation):
    """"
    Return thresholded 3d data and its cubulated version. 
    """
    # field on triangular grid
    field = xr.open_dataset(path + file)[var].squeeze().values
    # threshold field
    field = np.where(field<threshold, 0, 1)
    
    nlev = np.shape(field)[0]
    # determine size of array that holds cubulation
    array_size=0
    for ind in [0,1,2]:
        xlist=list()
        for entry in cubulation:
            xlist.append(entry[1][ind])
        array_size=max(array_size, max(xlist))
    array_size=array_size+1 # need to add one as cubulation indices start with 1 instead of 0
    # map field from triangular grid to field on nlev x cubic grid
    field_cube = np.zeros((nlev, array_size, array_size, array_size), dtype = 'byte')
    for lev in range(nlev):
        for entry in cubulation:
            triangle = entry[0]     # index of triangle
            cube = entry[1]         # cube coordinate
            field_cube[lev, cube[0], cube[1], cube[2]] = field[lev, triangle]
    
    return field, field_cube

# treat single level for data on multiple levels
def _field_icon_ilev(path, file, var, threshold, cubulation, ilev):
    """"
    Return thresholded 3d data and its cubulated version. 
    """
    # field on triangular grid, select single level
    field = xr.open_dataset(path + file)[var].rename({"height": "lev"}).isel(lev=ilev).squeeze().values
    # threshold field
    field = np.where(field<threshold, 0, 1)

    # determine size of array that holds cubulation
    array_size=0
    for ind in [0,1,2]:
        xlist=list()
        for entry in cubulation:
            xlist.append(entry[1][ind])
        array_size=max(array_size, max(xlist))
    array_size=array_size+1 # need to add one as cubulation indices start with 1 instead of 0
    # map field from triangular grid to field on nlev x cubic grid
    field_cube = np.zeros((array_size, array_size, array_size), dtype = 'byte')
    for entry in cubulation:
        triangle = entry[0]     # index of triangle
        cube = entry[1]         # cube coordinate
        field_cube[cube[0], cube[1], cube[2]] = field[triangle]
    
    return field, field_cube