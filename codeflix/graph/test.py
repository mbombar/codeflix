import generate_graph

def testgraphcreation():
    print('Testing create_graph_from_ids')
    G = generate_graph.create_graph_from_ids([1280])
    assert(len(G.edges()) == 2958)
    print('Testing create_graph')
    # DEBUG PHASE : IT'S TOO SLOW
    GG = generate_graph.create_graph()
    print(len(GG.edges()))
    print('Testing passed !')

testgraphcreation()
