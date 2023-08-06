# Implementation by means of graphs and networkx python library

import numpy as np
import xarray as xr
import networkx as nx


def prepare_grid(model, file):
    """
    Return required grid information as a xarray dataset.
    
       Input:
           model   string  model name
           file    string  name of the file containing the grid (including full path)
           
       Note that we only need the following information about the horizontal triangular grid:
           - the edge neighbors of a given triangle (for edge connectivity)
           - the triangles that share a given vertex (for vertex connectivity)
    """
    if model == "ICON":
        _grid = _grid_icon(file)
    return _grid


# implementation for ICON model
def _grid_icon(_gridfile):
    _grid = xr.open_dataset(_gridfile)
    _grid = _grid[["neighbor_cell_index", "cells_of_vertex"]]
    # in the ICON model grid, the indexing of the triangle cells and vertices 
    # starts with 1 and not with 0 as assumed by tricco --> we need to subtract 1 here
    _grid["neighbor_cell_index"] = _grid["neighbor_cell_index"] - 1
    _grid["cells_of_vertex"]     = _grid["cells_of_vertex"] - 1
    # after the substraction of 1, "missing" triangles at the border of the grid domain are indexed as -1
    # --> we set these values to -9999 to clearly flag these "missing" triangles
    _grid["neighbor_cell_index"] = xr.where(_grid["neighbor_cell_index"]!=-1, _grid["neighbor_cell_index"], -9999)
    _grid["cells_of_vertex"]     = xr.where(_grid["cells_of_vertex"]!=-1, _grid["cells_of_vertex"], -9999)
    return _grid


def compute_fullgraph(grid, connectivity="vertex"):
    """
    Returns full graph of the grid that contains all cells as nodes and with edges between all neighboring cells,
    depending on the type of connectivity
    
       Input:
          grid            xarray dataset    grid information
          connectivity    string            type of connectivity, either vertex or edge
    """
    ncells = grid.cell.size
    fgraph = nx.Graph()
    fgraph.add_nodes_from(range(0, ncells))
    # full graph for vertex connectivity
    if connectivity == "vertex":
        nverts = grid.vertex.size
        for vertex in range(0, nverts):
            cells_of_vertex = grid.cells_of_vertex[:, vertex].values
            for cell1 in cells_of_vertex:
                for cell2 in cells_of_vertex:
                    if cell1 >=0 and cell2>=0:
                        fgraph.add_edge(cell1, cell2)
    # full graph for edge connectivity
    elif connectivity == "edge":
        for cell in range(0, ncells):
            for neighbor in grid.neighbor_cell_index[:, cell].values:
                if neighbor >=0:
                    fgraph.add_edge(neighbor, cell)
    # unknown type of connectivity
    else:
        print("compute fullgraph: unknown type of connectivity:", connectivity, "--> full graph of grid not defined!")
        fgraph = None
    return fgraph


def compute_connected_components_2d(field, fgraph, threshold):
    """
    Returns connected components for 2-d data based on a thresholded field and the full graph of the grid.
        
        Input: 
            field : 1d-data for which connected components will be calculated, defined on each grid cell
            fgraph: full graph of the grid with all grid cells being nodes and edges defined between all neighboring
                    cells, hence the graph encodes whether edge of vertex connectivity will be considered
            threshold: set field to False if smaller than threshold, and to True otherwise
        Output: 
            list of connected components sorted by size of connected components (largest component first), 
            each connected component is a list of grid cells
    """
    # copy full graph to local graph
    _graph = fgraph.copy(as_view=False)
    # threshold field
    field = np.where(field<threshold, False, True)
    # remove grid cells/nodes from graph for which field < threshold, i.e., False
    for i in range(0, field.size):
        if not field[i]: _graph.remove_node(i)
    # compute connected components and sort by size
    components = []
    [components.append(list(cc)) for cc in nx.connected_components(_graph)];
    components = sorted(components, key=len, reverse=True)
    return components