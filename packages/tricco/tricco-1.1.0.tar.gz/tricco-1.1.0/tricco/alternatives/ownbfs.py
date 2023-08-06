# Implementation by means of a self-programmed breadth-first search

import numpy as np
import xarray as xr
from collections import deque  # for using lists as queues


def prepare_grid(model, file):
    """
    Return required grid information as a xarray dataset.
    
       Input:
           model   string  model name
           file    string  name of the file containing the grid (including full path)
           
       Note that we only need the following information about the horizontal triangular grid:
           - the edge neighbors of a given triangle (for edge connectivity)
           - the vertices of each triangle and the triangles that share a given vertex (for vertex connectivity)
    """
    if model == "ICON":
        _grid = _grid_icon(file)
    return _grid


# implementation for ICON model
def _grid_icon(_gridfile):
    _grid = xr.open_dataset(_gridfile)
    _grid = _grid[["neighbor_cell_index", "vertex_of_cell", "cells_of_vertex"]]
    # in the ICON model grid, the indexing of the triangle cells and vertices 
    # starts with 1 and not with 0 as assumed by tricco --> we need to subtract 1 here
    _grid["neighbor_cell_index"] = _grid["neighbor_cell_index"] - 1
    _grid["vertex_of_cell"] = _grid["vertex_of_cell"] - 1
    _grid["cells_of_vertex"] = _grid["cells_of_vertex"] - 1
    # after the substraction of 1, "missing" triangles at the border of the grid domain are indexed as -1
    # --> we set these values to -9999 to clearly flag these "missing" triangles
    _grid["neighbor_cell_index"] = xr.where(_grid["neighbor_cell_index"]!=-1, _grid["neighbor_cell_index"], -9999)
    _grid["vertex_of_cell"] = xr.where(_grid["vertex_of_cell"]!=-1, _grid["vertex_of_cell"], -9999)
    _grid["cells_of_vertex"] = xr.where(_grid["cells_of_vertex"]!=-1, _grid["cells_of_vertex"], -9999)
    return _grid


def _add_neighbors_to_queue(cell, field, grid, connectivity, explored, queue):
    """
    Add neighbors of a given cell to the queue if they are in the same connected component and not yet explored.
    
       Input: 
           cell            int               the index of the cell currently considered
           field           numpy array       thresholded 1-d array with values of True or False,
                                             defined on each grid cell
           grid            xarray dataset    grid information
           connectivity    string            type of connectivity, either vertex or edge
           explored        1-darray          information on whether cells have been explored yet
       Input/Output:
           queue           list-queue        cell indices for breadth-first search of current connected component
    """
    ncells=field.size
    # vertex connectivity
    if connectivity == "vertex":
        vertex_of_cell = grid.vertex_of_cell[:, cell].values
        for vertex in vertex_of_cell:
            for neigh in grid.cells_of_vertex[:,vertex].values:
                if neigh!=cell and neigh>=0 and field[neigh] and not explored[neigh] and neigh not in queue:
                    queue.append(neigh)
    # edge connectivity
    elif connectivity == "edge":
        for neigh in grid.neighbor_cell_index[:, cell].values:
            if neigh>=0 and field[neigh] and not explored[neigh] and neigh not in queue:
                queue.append(neigh)
    # unknown type of connectivity
    else:
        print("_add_neighbors_to_queue: unknown type of connectivity:", connectivity, "--> ownbfs cannot work!")
    

def compute_components_2d(grid, field, threshold, connectivity="vertex"):
    """
    Returns connected components for given grid, field and connectivity type.
    
        The implementation runs through all cells. If a cell is not yet explored and has a value>=threshold, then
        its connected component is explored via breadth-first-search marking all considered cells as explored. 
    
        Input: 
        
            grid            xarray dataset    grid information
            field           numpy array       1-d array of field for which connected components will be calculated,
                                              defined on each grid cell
            threshold       float             set field to False if smaller than threshold, and to True otherwise
            connectivity    string            type of connectivity, either vertex or edge
            
        Output: 
            list of connected components sorted by size of connected components (largest component first), 
            each connected component is a list of grid cells
    """
    ncells = field.size
    # threshold field
    field = np.where(field<threshold, False, True)
    # init lists for connected components and explored cells
    components = []
    explored = [False] * ncells
    # loop over all cells
    for cell in range(ncells):
        if not explored[cell]:  # cell must not be explored yet
            explored[cell] = True
            if field[cell]:  # if cell is covered, it belongs to a new connected component
                # init component list and queue for BFS of this connected component
                comp = [cell]
                queue = deque([])
                _add_neighbors_to_queue(cell, field, grid, connectivity, explored, queue)
                # perform BFS
                while queue:
                    cell = queue.pop()
                    explored[cell] = True
                    comp.append(cell)
                    _add_neighbors_to_queue(cell, field, grid, connectivity, explored, queue)
                # append found component to list of components
                components.append(comp)
    # sort connected components by size, starting with the largest component
    components = sorted(components, key=len, reverse=True)
    return components