import argparse
import sys

sys.path.append('../')
from api import api  # noqa: E402
from graph import generate_graph  # noqa: E402
import networkx as nx  # noqa: E402
import recommendation as rec  # noqa: E402


def createtestgraph():
    g = nx.Graph()
    g.add_edge('Alice', '1', weight=0)
    g.add_edge('Bob', '1', weight=0)
    g.add_edge('Bob', '2', weight=0.9)
    g.add_edge('Charlie', '1', weight=1)
    g.add_edge('Charlie', '2', weight=0)
    g.add_edge('Charlie', '3', weight=1)
    return g


def testscore():
    g = createtestgraph()
    assert(rec.score('Alice', 'Bob', g) == 1)
    assert(rec.score('Alice', 'Charlie', g) == -1)
    assert(rec.score('Bob', 'Charlie', g) == -1.8)


def testnearest():
    g = createtestgraph()
    users = ['Alice', 'Bob', 'Charlie']
    ans = rec.knearestusers('Alice', 1, users, g)
    assert(ans == ['Bob'])


def testrecommendation():
    g = createtestgraph()
    users = ['Alice', 'Bob', 'Charlie']
    recommended = rec.recommendation('Alice', users, g, 1, debug = False)
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
    (g, users, problems) = generate_graph.create_graph(check=False, verbose=False)
    print("Done !")
    print("Computing recommendation")
    sortedproblems = rec.recommendation(user, users, g)
    print("Number of recommended problems : {}".format(len(sortedproblems)))
    problem = api.Problem.objects.filter(name=sortedproblems[0]).first()
    print("We recommend {} to try and solve problem {} : https://codeforces.com/problemset/problem/{}/{}".format(user, problem, problem.contest_id, problem.index))
    print('Testing passed !')


parser = argparse.ArgumentParser("Tests for codeflix recommendation system")

parser.add_argument("-r", "--real", action="store_true", help="Do a test with real values")
parser.add_argument("-u", "--user", action="store", help="Specify a user", default="LeCaRiBoU")

if __name__ == "__main__":
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
