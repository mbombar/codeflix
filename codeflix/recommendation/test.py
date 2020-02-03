import recommendation as rec
import networkx as nx

import sys
sys.path.append('../')
from graph import generate_graph
from api import api

import argparse

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
    recommended = rec.recommendation('Alice', users, G, 1)
    assert(recommended == ['2'])

def testeverything():
    print('Testing score')
    testscore()
    print('Testing knearestusers')
    testnearest()
    print('Testing recommendations')
    testrecommendation()
    print('Testing passed !')

def realtest(user='LeCaRiBoU'):
    print("Doing a test with real values")
    print("Generating graph ...")
    (G, users, problems) = generate_graph.create_graph(check=False, verbose=False)
    print("Done !")
    print("Computing recommendation")
    sortedproblems = rec.recommendation(user, users, G)
    print("Number of recommended problems : {}".format(len(sortedproblems)))
    problem = api.Problem.objects.filter(name=sortedproblems[0]).first()
    print("We recommand {} to try and solve problem {} : https://codeforces.com/problemset/problem/{}/{}".format(user, problem, problem.contest_id, problem.index)) # Fix URL for old problems...
    print('Testing passed !')


parser = argparse.ArgumentParser("Tests for codeflix recommendation system")

parser.add_argument("-r", "--real", action="store_true", help="Do a test with real values")
parser.add_argument("-u", "--user", action="store", help="Specify a user", default="LeCaRiBoU")

if __name__=="__main__":
    args = parser.parse_args()
    if args.real:
        user = args.user
        check = bool(api.CodeforcesUser.objects.filter(handle=user))
        if not check:
            print("Unknown user {}".format(user))
        else:
            print("Doing recommendation for user {}".format(user))
            realtest(user)
    else:
        testeverything()
