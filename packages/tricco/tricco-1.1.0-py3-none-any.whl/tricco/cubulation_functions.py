import numpy as np
import cc3d # external library for connected component labeling on cubic grids

from .grid_functions import get_vertices_of_edge, get_edges_of_cell, get_neighbors_of_cell


class EnhancedTri:
    """
    class to enhance a triangle with its cube coordinate
    for a given triangle create an object consisting of the triangle index and the triangle's cube coordinate
    """
    def __init__(self, triangle, cube):
        self.triangle = triangle
        self.cube = cube
    def print(self):
        print("Triangle index:", self.triangle, " Cube coordinate:", self.cube)
        

def colour_exactly_one_new_edge(first_known_edge, second_known_edge, new_edge, edge_colours):
    """
    Colouring edges of a triangle
    Situation:  the colours of two edges are already known, 
                the third edge must be coloured
    called from colour_new_edges in this special situation
   
        Input:
            first_known_edge      int     index of a already coloured edge
            second_known_edge     int     index of a already coloured edge
            new_edge              int     index of the not yet coloured edge
            edge_colours          dict    dictionary storing to each edge index the colour
        Output:
            none, but updates edge_colours
    """    
    # get the colours of the already coloured edges
    first_colour = edge_colours[first_known_edge]
    second_colour = edge_colours[second_known_edge]
    
    # determine new colour, i.e. the one not taken from (0,1,2) by first_colour and second_colour
    for i in (0,1,2): 
        if not (first_colour == i or second_colour == i):
            edge_colours[new_edge] = i  # colour found -> update edge_colours
            return
        
        
def colour_new_edges(old_triangle_edges, new_triangle_edges, joint_edge, edge_colours):
    """
    Colouring edges of a triangle
    From old_triangle with already coloured edges determine the edge_colours of the adjacent new_triangle

        Input:
            old_triangle_edges      set     contains the edge indices of old_triangle's edges
            new_triangle_edges      set     contains the edge indices of new_triangle's edges
            joint_edge              int     index of the shared edge from old_triangle and new_triangle
            edge_colours            dict    dictionary storing to each edge index the colour
        Output:
            none, but updates edge_colours
    """    
    # determine the edges of new_triangle that are not shared with old_triangle
    new_edges   = new_triangle_edges.difference( old_triangle_edges ) 
    first_edge  = new_edges.pop()
    second_edge = new_edges.pop()
    
    # are the found edges uncoloured?
    first_is_coloured = first_edge in edge_colours
    second_is_coloured = second_edge in edge_colours
    
    # case: first_edge is coloured
    if first_is_coloured: 
        if second_is_coloured: 
            return # both known -> nothing to colour
        else: 
            # colour second_edge using the colours of first_edge and joint_edge
            colour_exactly_one_new_edge( first_edge, joint_edge, second_edge, edge_colours )
    
    # case: second_edge is coloured
    if second_is_coloured: 
        # colour first_edge using the colours of second_edge and joint_edge
        colour_exactly_one_new_edge( second_edge, joint_edge, first_edge, edge_colours )
    
    # case: both edges are uncoloured
    else: 
        # get old_triangle's edges that are not joined with new_triangle
        comparison_edges = old_triangle_edges.difference( new_triangle_edges )
        first_comparison_edge = comparison_edges.pop()
        second_comparison_edge = comparison_edges.pop()
        
        # get vertices of first_edge and first_comparison_edge
        first_vertices = get_vertices_of_edge( first_edge )
        first_comparison_vertices = get_vertices_of_edge( first_comparison_edge )
        
        # if first_edge and first_comparison_edge have no shared vertices:
        #   the two edges must be parallel and thus, have the same colour
        #   else, first_edge must be parallel to second_comparison_edge and thus, have the same colour
        parallel = set(first_vertices).isdisjoint( set(first_comparison_vertices) )
        
        if parallel: # parallel: same colour
            edge_colours[ first_edge ] = edge_colours[ first_comparison_edge ]
            edge_colours[ second_edge ] = edge_colours[ second_comparison_edge ] 
        
        else: # not parallel: first_edge and second_comparison_edge are parallel and same-coloured
            edge_colours[ first_edge ] = edge_colours[ second_comparison_edge ]
            edge_colours[ second_edge ] = edge_colours[ first_comparison_edge ]
            
        
def determine_cube_coordinates (old, old_triangle_edges, new_triangle_edges, joint_edge, edge_colours):
    """
    Compute cube coordinate of a new triangle
    Given the old_triangle's cube_coordinate derive the cube coordinate of the adjacent new_triangle 
    by using the colour of their joint_edge 

        Input:
            old                     EnhancedTri     the old EnhancedTri with known cube_coordinates
            joint_edge              int             index of the shared edge from old_triangle and new_triangle
            edge_colours            dict            dictionary storing to each edge index the colour

        Output:
            new_cube_coordinate, the cube_coordinate of new_triangle
    """    
    # get colour of the joint_edge and call it direction
    direction = edge_colours[joint_edge]
    # the direction encodes the parallel class of the joint edge
    # this encodes also the direction in which one has to walk from old_triangle to new_triangle
    # this gives the coordinate in which the cube_coordinates of old_- and new_triangle differ
    
    # determine direction-vector (1,0,0), (0,1,0) or (0,0,1) by which the cube_coordinates will differ
    direction_vector = np.array([0,0,0])
    direction_vector[direction] = 1 
    
    # use invariant: sum of coordinates musst be 0 or 1
    # determine wether the direction vector has to be added or subtracted
    # by using the invariant that the sum of all valid cube_coordinates has to be 0 or 1
    old_coordinate_sum = sum(old.cube[i] for i in (0,1,2))
    if old_coordinate_sum == 0:
        # old triangle's coordinate sum is 0 thus new ones has to be 1 -> add
        new_cube_coordinate = old.cube + direction_vector
    else: 
        # old triangle's coordinate sum is 1 thus new ones has to be 0 -> subtract
        new_cube_coordinate = old.cube - direction_vector
    
    return new_cube_coordinate


def cubing_next_round(cube_coordinates, visited_triangles, outmost, edge_colours):
    """
    Iterate over the outmost triangles and compute the cube_coordinates of their adjacent triangles
    
        Input:
            cube_coordinates        array       EnhancedTri's of the triangles whose cube_coordinates are already computed
            visited_triangles       list        indices of the triangles whose cube_coordinates are already computed
            outmost                 list        EnhancedTri's of the triangles considered in the round before   
            edge_colours            dict        dictionary storing to each edge index the colour
        Output:
            updated outmost, EnhancedTri's of the new triangles considered this round
    """    
    # list for triangles that will be outmost in next iteration
    new_outmost = []
   
    for old in outmost: # consider all EnhancedTri's at the border of visited
        for neigh in get_neighbors_of_cell(old.triangle ): # consider all neighbours
            new = EnhancedTri(neigh, 0)

            if new.triangle != -9999: # ommit missing triangles that occur at the grid border (marked by -9999)
                if new.triangle not in visited_triangles: # EnhancedTri new has no cube_coordinate yet

                    # add new to new_outmost for next round hereafter and update visited_triangles
                    new_outmost.append( new )
                    visited_triangles.append ( new.triangle )

                    # preparation: obtain edges of new_triangle and old_triangle and derive their joint_edge
                    old_triangle_edges = set(get_edges_of_cell(old.triangle)) # this is a set for python reasons...
                    new_triangle_edges = set(get_edges_of_cell(new.triangle))
                    joint_edge = ( new_triangle_edges & old_triangle_edges ).pop()

                    # colour the edges of new.triangle
                    colour_new_edges (old_triangle_edges, new_triangle_edges, joint_edge, edge_colours)

                    # get cube coordinates for EnhancedTri new and update the array of cube_coordinates
                    new.cube = determine_cube_coordinates (old, old_triangle_edges, new_triangle_edges, joint_edge, edge_colours)
                    cube_coordinates.append(np.array([new.triangle, new.cube], dtype=object))
    
    return new_outmost


def shift_coordinates (cube_coordinates, radius):
    """
    Shift cube coordinates such that they are all positive

        Input:
            cube_coordinates    array   stores triangle - cube_coordinate pairs
            radius              int     same as in compute_cube_coordiantes
        
        Output:
            shifted cube_coordinates
    """
    shift = int(radius/2)
    # update all coordinates
    for entry in cube_coordinates:
        cube = entry[1] # get cube_coordinate 
        # consider all three directions
        for direction in (0,1,2):
            cube[direction] += shift # shift coordinate
    return cube_coordinates


def compute_connected_components(field_cube, connectivity = 'vertex'):
    """
    Compute connected components
    
        Input:
            field_cube     array    obtained as part of field prepaation
            connectivity   string   use 'vertex' (default) or 'edge' connectivity
        Output:
            component_cube, 3d array containing the component indices
    """    
    import sys
    # translate connectivity - string into input value for 3d connected component labeling
    if connectivity == 'edge':
        connectivity_value = 6
    else:
        connectivity_value = 26     
        if connectivity != 'vertex':    # use default 'vertex' connectivity for invalid input
            sys.exit("Invalid input: only 'vertex' or 'edge' connectivity are allowed.")
    # calling external 3d connected component labeling
    component_cube = cc3d.connected_components(field_cube, connectivity = connectivity_value)
    return component_cube


def compute_list_of_components(cubulation, component_cube):
    """
    Which triangle belongs to which component?
        
        Input:
            cubulation         array       output of compute_cube_coordinates   
            component_cube     3d arry     output of compute_connected_components
        
        Output:
            Returns a list of lists. 
            Each inner list corresponds to one connected component and contains the indices
            of all triangles that belong to it.
    """
    # number of found components on cubical grid
    ncomp = component_cube.max()
    
    # initialize list of ncomp lists, with each list holding the triangles that
    # belong to a specific connected component
    component_list = []
    for n in range(ncomp):
        component_list.append([])
    
    # determine component
    for entry in cubulation:
        triangle  = entry[0]        # index of triangle
        cube      = entry[1]        # cube coordinate
        component = component_cube[cube[0]][cube[1]][cube[2]]
        if component != 0:  # triangle belongs to a connected component
            # add triangle to its component list
            component_list[component-1].append(triangle)
    
    return component_list
