import sys
sys.path.append("../")

from api import api  # noqa: E402
from graph import generate_graph  # noqa: E402


def score(user, otheruser, g):
    ans = 0
    for pb in g[user]:
        if g.has_edge(otheruser, pb):
            wuser = g[user][pb]['weight']
            wotheruser = g[otheruser][pb]['weight']
            ans += (2 * wuser - 1) * (2 * wotheruser - 1)
    return ans


def knearestusers(user, k, userslist, g):
    nearestusers = []
    for otheruser in userslist:
        if otheruser != user:
            nearestusers.append((score(user, otheruser, g), otheruser))
    nearestusers.sort()
    return [otheruser for (_, otheruser) in nearestusers[len(nearestusers) - k:]]


def sortscoreproblems(user, users, g):
    sumproblems = dict()
    nbproblems = dict()
    for u in users:
        for problem in g[u]:
            sumproblems[problem] = sumproblems.get(problem, 0) + g[u][problem]['weight']
            nbproblems[problem] = nbproblems.get(problem, 0) + 1
    scoredpbs = []
    for pb in sumproblems.keys():
        if (pb not in g[user]) or (g[user][pb]['weight'] == 1):
            scoredpbs.append((sumproblems[pb] / nbproblems[pb], pb))
    scoredpbs = list(sorted(filter(lambda x: x[0] < 1, scoredpbs), reverse=True))
    return list(map(lambda x : x[1], scoredpbs))


def recommendation(user, users, g, kusers=20):
    nearestusers = knearestusers(user, kusers, users, g)
    sortedproblems = sortscoreproblems(user, nearestusers, g)
    return sortedproblems


def displayrecommendation(user, graph=None, nb=[0], kusers=20):
    if isinstance(nb, int):
        nb = [nb]
    if not graph:
        graph = generate_graph.create_graph(check=False, verbose=False)
    (g, users, problems) = graph
    sortedproblems = recommendation(user, users, g)
    for x in nb:
        problem = api.Problem.objects.filter(name=sortedproblems[x]).first()
        print("We recommend {} to try and solve problem {} : https://codeforces.com/contest/{cid}/problem/{index}".format(user, problem, cid=problem.contest_id, index=problem.index))
