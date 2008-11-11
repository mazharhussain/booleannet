#
#
# demonstrate the use of the time model
#
# generates a transition graph for all possible initial conditions
#

import boolean2
from boolean2 import state, network
from networkx import component

def simulation( ):

    # creating the transition graph, the verbose parameter sets the nodes to 
    # either short names like 1, 2, 3 or long (binary) names like 10001
    #
    # the logfile contains the transition edges and the identity of the nodes
    trans = network.TransGraph( logfile='timemodel.log', verbose=True )

    # create the model, you may use a text string or a filename
    model = boolean2.Model( text='timemodel.txt', mode='time')

    
    # here we generates all initial states
    #
    # IMPORTANT: Only uninitialized nodes will get new values,
    # to keep a node the same in all iterations initialize it in the rules
    #
    # when the limit parameter is a number it will takes the first that 
    # many initial values, leave it to None to use all initial values
    initializer = state.all_initial_states( model.nodes, limit=None )

    # the data is a dictionary with the inital data, print it to see what it contains
    # the initfunc is the initializer function that can be used
    for data, initfunc in initializer:
        model.initialize( missing=initfunc )
        model.iterate( 12 )
        trans.add( model.states )

   
    # if you need to access the networkx graph for further processing
    # us the graph attribute of the trans object
    
    # a list of colors in hexadecimal Red/Gree/Blue notation
    colors = [ '#FF0000', '#00FF00', '#0000FF', '#ACDE00', '#F0F0F0' ]
    
    # find the strongly connected components
    components = component.strongly_connected_components( trans.graph)

    # make sure we have as many colors as components
    if len(colors) < len(components):
        print 'NOTE: there are more components than colors!'
    
    # need to set up a colormap, a dictionary that contains a node -> color
    # or edge -> color values
    colormap = {}
    for color, comp in  zip(colors, components):
        print 'setting color %s for component %s' % (color, comp)
        for node in comp:
            colormap[node] = color

    # saves the transition graph into a gml file, 
    # leave off the colormap if nodes or edges do not need to be colored
    trans.save( fname='timemodel.gml', colormap=colormap )

# this runs the simulation
if __name__ == '__main__':
    simulation()