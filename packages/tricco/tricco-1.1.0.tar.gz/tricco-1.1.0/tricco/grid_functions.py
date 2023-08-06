# xarray dataset that holds the grid
grid = None

def get_neighbors_of_cell(triangle):
    """
    Returns edge neighbors of a given triangle
    """
    return grid.neighbor_cell_index[:,triangle].values
   
def get_edges_of_cell(triangle):
    """
    Returns the three edges of a given triangle
    """
    return grid.edge_of_cell[:, triangle].values


def get_vertices_of_edge(edge):
    """
    Returns the two vertices of a given edge
    """
    return grid.edge_vertices[:, edge].values
