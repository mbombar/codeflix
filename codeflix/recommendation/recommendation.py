import networkx as nx

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

def rankscoreproblems(user, users, G):
    sumproblems = dict()
    nbproblems = dict()
    for user in users:
        for problem in G[user]:
            if problem not in sumproblems:
                sumproblems[problem] = 0
                nbproblems[problem] = 0
            sumproblems[problem] += G[user][problem]['weight']
            nbproblems[problem] += 1
    l = []
    for pb in sumproblems.keys():
        if (pb not in G[user]) or (G[user][pb]['weight'] == 1):
            l.append((sumproblems[pb] / nbproblems[pb],pb))
    l.sort()
    l.reverse()
    return list(map(lambda x : x[1], l))

def recommendation(user, users, G, kusers, kproblems):
    nearestusers = knearestusers(user, kusers, users, G)
    rankedproblems = rankscoreproblems(user, nearestusers, G)
    return rankedproblems[:kproblems]
