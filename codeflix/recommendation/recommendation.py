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
