import generate_graph

def testgraphcreation():
    print('Testing create_graph_from_ids')
    (G, users, problems) = generate_graph.create_graph_from_ids([1280], verbose=True)
    assert(len(G.edges()) == 2958)
    print('Testing create_graph')
    # DEBUG PHASE : IT'S TOO SLOW
    (finalG, finalusers, finalproblems) = generate_graph.create_graph(check=False, verbose=True)
    print(len(finalG.edges()))
    print('Testing passed !')

testgraphcreation()
