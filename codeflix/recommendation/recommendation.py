import networkx as nx
import sys
sys.path.append("../")
from graph import generate_graph
from api import api

def score(user, otheruser, G):
    ans = 0
    for pb in G[user]:
        if G.has_edge(otheruser, pb):
            wuser = G[user][pb]['weight']
            wotheruser = G[otheruser][pb]['weight']
            ans += (2 * wuser- 1) * (2 * wotheruser - 1)
    return ans

def knearestusers(user, k, userslist, G):
    l = []
    for otheruser in userslist:
        if otheruser != user:
            l.append((score(user, otheruser, G), otheruser))
    l.sort()
    return [otheruser for (_, otheruser) in l[len(l) - k:]]

def sortscoreproblems(user, users, G):
    sumproblems = dict()
    nbproblems = dict()
    for u in users:
        for problem in G[u]:
            sumproblems[problem] = sumproblems.get(problem, 0) + G[u][problem]['weight']
            nbproblems[problem] = nbproblems.get(problem, 0) + 1
    l = []
    for pb in sumproblems.keys():
        if (pb not in G[user]) or (G[user][pb]['weight'] == 1):
            l.append((sumproblems[pb] / nbproblems[pb],pb))
    l = list(sorted(filter(lambda x: x[0] < 1, l), reverse=True))
    return list(map(lambda x : x[1], l))

def recommendation(user, users, G, kusers = 20):
    nearestusers = knearestusers(user, kusers, users, G)
    sortedproblems = sortscoreproblems(user, nearestusers, G)
    return sortedproblems


def displayrecommendation(user, graph=None, nb=[0], kusers = 20):
    if isinstance(nb, int):
        nb = [nb]
    if not graph:
        graph = generate_graph.create_graph(check=False, verbose=False)
    (G, users, problems) = graph
    sortedproblems = recommendation(user, users, G)
    for x in nb:
        problem = api.Problem.objects.filter(name=sortedproblems[x]).first()
        print("We recommend {} to try and solve problem {} : https://codeforces.com/contest/{cid}/problem/{index}".format(user, problem, cid=problem.contest_id, index=problem.index))
