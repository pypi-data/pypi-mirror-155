import numpy as np
    
from .grid_functions import get_edges_of_cell
from .cubulation_functions import EnhancedTri, cubing_next_round, shift_coordinates, compute_connected_components, compute_list_of_components 


def compute_cubulation(start_triangle, radius, print_progress=False): 
    """
    Assign to each triangle a 3d-coordinate called cube coordinate.
       
        Input: 
            start_triangle      int         the triangle index where the cubulatiion algorithm starts
            radius              int         the number of "outward" steps
            print_progress      Boolean     print progress of iteration (default False)
     
        Output: 
            Returns a list of arrays of the following form:
            np.array([<triangle index>, <cube array>])
            where <cube array> is an array with three entries that encode the cube coordinate of the triangle with <triangle index>. 
    """
    # initialization
    init = EnhancedTri(start_triangle, np.array([0,0,0])) # assign coordinates (0,0,0) to start_triangle
    cube_coordinates = [np.array([init.triangle, init.cube], dtype=object)]
    visited_triangles = [init.triangle]
    outmost = [init] # list for EnhancedTri that were added last round and thus lie "at the boundary of discovery"
    
    # colour the edges of start_triangle with 0,1,2
    edge_colours = { get_edges_of_cell(start_triangle)[x] : x for x in (0,1,2) }
    
    # expand outwards 
    for n in range(radius):
        # update outmost triangles
        outmost = cubing_next_round(cube_coordinates, visited_triangles, outmost, edge_colours)
        # optional: show progress
        if print_progress: print("Round ", n+1, "finished. Visited ", len(cube_coordinates), \
                                 "triangles, thereof ", len(outmost), "new.")
    
    # return coordinates after shifting them to positivity
    return shift_coordinates(cube_coordinates, radius)
    
    
def compute_connected_components_2d(cubulation, field_cube, connectivity = "vertex"): 
    """
    From given cubuluation, compute connected components and output them as a list of lists

        Input:
            cubulation          list of arrays      output of compute_cubulation 
            field_cube          numpy array         input field in cubulated 3d-coordinates
            connectivity        string              use 'vertex' (default) or 'edge' connectivity
        Output: 
            - Returns a list of lists. 
            - Each inner list corresponds to a connected component and contains 
              all triangle indices that belong to this connected component
    """    
    # compute connected components on field_cube
    # components_cube is a 3-dimensional array that contains
    # the connected component index of a triangle with cube coordinates (x,y,z) at position component_array[x][y][z]
    components_cube = compute_connected_components(field_cube, connectivity)
    
    # a component list of triangle indices is generated for each connected component:
    # returns a list containing all component lists
    components = compute_list_of_components(cubulation, components_cube)
   
    return components


def compute_connected_components_3d(cubulation, field_cube, connectivity = "vertex"):
    """
    From given cubuluation, compute connected components and output them as a list of lists
   
        Input:
            cubulation          list of arrays      output of compute_cubulation 
            field_cube          numpy array         input field in dimensions of (lev x cubulated coordinates)
            connectivity        string              use 'vertex' (default) or 'edge' connectivity
 
        Output: 
            - Returns a list of lists. 
            - Each inner list corresponds to a connected component and contains all tuples of (level, triangle index) that
              belong to this connected component
    """    
    nlev = np.shape(field_cube)[0] # number of vertical levels
    
    # Compute connected components for each level separately, 
    # in the following these are refered to as 2d connected components.
    components2d = []
    for lev in range(nlev):
        aux = compute_connected_components_2d(cubulation, field_cube[lev], connectivity)
        for items in aux:
            components2d.append([lev]+sorted(items))
    del aux
    
    # Merge connected components in the vertical
    components3d = compute_levelmerging(components2d, nlev)
    
    return components3d


def compute_levelmerging(components2d, nlev):
    """
    From a list of connected components per level, merge components that are connected over levels. 
    This will yield the connected components in the 3-dimensional space (i.e., the 3d connected components).
    To achieve this, we regard each 2d connected component as a node of an undirected graph and 
    use the connected component finding for graphs as implemented by networkx.
   
        Input:
            components2d         list of lists     connected components per level, each inner list is a 2d connected
                                                   component with the level as its first entry followed by the indices of 
                                                   connected cells on that level 
                                                   --> e.g., components[20] = [lev, 1058, 1059, 2099, 2100, ... ]
            nlev                  int              number of levels
            
        Output: 
            components_3d         list of lists    connected components merged over levels, each inner list 
                                                   corresponds to a connected component and contains all 
                                                   tuples of (level, cell index) that belong to it
    """    
    # Look for connections between nodes, i.e., cases when two 2d connected compoents
    # are in adjacent levels and share at least one cell with each other.
    # This creates a list of pairs that uses the indices components2d and are the edges of the graph
    # ---> e.g., a pair might lool like pairs[0] = [0,1], in which case if would consist
    #      of the first and second inner list of components2d
    pairs =set() # we make use of sets as it automatically removes duplicate pairs
    for item1 in components2d:
        for item2 in components2d:
            if np.abs(item1[0]-item2[0])==1: # the two 2d connected components need to be adjacent in the vertical
            # is there overlap between the two 2d connected components?
                if not set(item1[1:]).isdisjoint(item2[1:]): # --> enter if there is overlap
                    pair = tuple(sorted([components2d.index(item1), components2d.index(item2)]))
                    pairs.add(pair)
    # turn pairs into a sorted list 
    pairs = sorted(list(pairs))   

    # we use the implmentation of the networkx library; this choice is 
    # inspired by https://stackoverflow.com/a/62545221/10376696
    import networkx as nx
    # create ubdirected graph based on its edges, which are defined by pairs
    graph = nx.Graph(pairs)
   
    # We also add all 2d connected components as nodes. This is needed
    # to catch cases when a 2d connected component is not connected to another 2d connected
    # components in a level above or below, i.e., it does not appear in "pairs".
    graph.add_nodes_from(range(0, len(components2d)))
                        
    # We now use connected component search on the graph to identify 2d connected components 
    # that belong together.
    # --> E.g., assume the graph consists of graph.nodes=[0, 1, 100] and 
    #     graph.edges=[(0,1), (0,2), (1,3), (3,4), (7,8), (7,10), (10,11), (15,16), (20,24)],
    #     then this should result in [{100}, {0,1,2,3,4}, {7,8,10,11}, {15,16}, {20,24}].
    #     That is, there are five 3d connected components.
    # "result" is a list of sets, which each set defining a 3d connected component.
    # For each set, the entries refer to the indices of components2d.
    result = list(nx.connected_components(graph))
    del graph
    
    # Finally, we create the list of 3d connected components, with each
    # 3d connected component being given as a sublist of (lev, triangle) tuples.
    components3d=list()
    # loop over the sets of result
    for cc3d in result:
        cc3d_tuples = [] # a list of (lev, triangle) tuples that belong to this 3d connected component
        # loop over the 2d connected components, or more precisely their indices in the list components
        for cc2d in cc3d: 
            # loop over the triangles that belong to a 2d connected component,
            # remember that the first entry is the level (see step 1)
            lev = (components2d[cc2d])[0]
            tri = (components2d[cc2d])[1:]
            for ind_tri in tri: 
                # generate the tuples and append them to the list cc3d_tuples that define the 3d connected component
                aux = tuple((lev,ind_tri))
                cc3d_tuples.append(aux)
        components3d.append(cc3d_tuples)
    
    return components3d