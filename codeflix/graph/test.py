import generate_graph

def testgraphcreation():
    print('Testing create_graph_from_ids')
    G = generate_graph.create_graph_from_ids([1280])
    assert(len(G.edges()) == 9126)
    print('Testing passed !')

testgraphcreation()
