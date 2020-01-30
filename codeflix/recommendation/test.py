import recommendation as rec
import networkx as nx

def createtestgraph():
    G = nx.Graph()
    G.add_edge('Alice', '1', weight=0)
    G.add_edge('Bob', '1', weight=0)
    G.add_edge('Bob', '2', weight=1)
    G.add_edge('Charlie', '1', weight=1)
    G.add_edge('Charlie', '2', weight=0)
    G.add_edge('Charlie', '3', weight=1)
    return G

def testscore():
    G = createtestgraph()
    assert(rec.score('Alice', 'Bob', G) == 1)
    assert(rec.score('Alice', 'Charlie', G) == -1)
    assert(rec.score('Bob', 'Charlie', G) == -2)

def testnearest():
    G = createtestgraph()
    users = ['Alice', 'Bob', 'Charlie']
    ans = rec.knearestusers('Alice', 1, users, G)
    assert(ans == ['Bob'])

def testrecommendation():
    G = createtestgraph()
    users = ['Alice', 'Bob', 'Charlie']
    recommended = rec.recommendation('Alice', users, G, 1, 1)
    assert(recommended == ['2'])

def testeverything():
    print('Testing score')
    testscore()
    print('Testing knearestusers')
    testnearest()
    print('Testing recommendations')
    testrecommendation()
    print('Testing passed !')

testeverything()
