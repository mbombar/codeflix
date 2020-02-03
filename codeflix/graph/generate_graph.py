import sys
import time

if '../' not in sys.path:
    sys.path.append('../')

from api import api
import networkx as nx

def add_edge(user, problem, solved, G):
    if solved or not G.has_edge(user,problem):
        G.add_edge(user, problem, weight=(0 if solved else 1))

def add_contest(contestid, G, users_set, pbs_set):
    (solves, users, pbs) = api.solvedsubmissionsduringcontest(contestid)
    for pb in pbs:
        pbs_set.add(pb)
    for user in users:
        users_set.add(user)
        for pb in pbs:
            add_edge(user, pb, False, G)
    for (user, pb) in solves:
        add_edge(user, pb, True, G)

def create_graph_from_ids(contestids, verbose=True):
    G = nx.Graph()
    users = set()
    problems = set()
    for contestid in contestids:
        if verbose:
            # USED FOR TESTING
            print('NEW CONTEST ' + str(contestid))
        add_contest(contestid, G, users, problems)
    return (G, users, problems)

def create_graph(check=True, verbose=True):
    contestslist = api.getcontestslist()
    contestsids = api.getcontestidslist(contestslist)
    usefulids = api.filterusefulcontests(contestsids, check)
    return create_graph_from_ids(usefulids, verbose)
