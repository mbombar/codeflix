import sys

if '../' not in sys.path:
    sys.path.append('../api')

import api
import networkx as nx

def add_edge(user, problem, solved, G):
    if solved or not G.has_edge(user,problem):
        G.add_edge(user, problem, weight=(0 if solved else 1))

def add_contest(contestid, G):
    # USED FOR TESTING
    print('NEW CONTEST')
    (solves, users, pbs) = api.solvedsubmissionsfromid(contestid)
    for user in users:
        for pb in pbs:
            add_edge(user, pb, False, G)
    for (user, pb) in solves:
        add_edge(user, pb, True, G)

def create_graph_from_ids(contestids):
    G = nx.Graph()
    for contestid in contestids:
        add_contest(contestid, G)
    return G

def create_graph():
    contestslist = api.getcontestslist()
    contestsids = api.getcontestidslist(contestslist)
    usefulids = api.filterusefulcontests(contestsids)
    return create_graph_from_ids(usefulids)
