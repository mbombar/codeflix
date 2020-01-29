import api
import networkx as nx

def add_edge(user, problem, solved, G):
    if solved or not G.has_edge(user,problem):
        G.add_edge(user, problem, weight=(0 if solved else 1))

def add_contest(contestid, G):
    submissionslist = api.getsubmissionslist(contestid)
    (solves, users, pbs) = api.solvedsubmissions(submissionslist)
    for user in users:
        for pb in pbs:
            add_edge(user, pb, False, G)
    for (user, pb) in solves:
        add_edge(user, pb, True, G)

def create_graph():
    G = nx.Graph()
    contestslist = api.getcontestslist()
    contestsids = api.getcontestidslist(contestslist)
    usefulids = api.filterusefulcontests(contestsids)
    for contestid in usefulids:
        add_contest(contestid, G)
    return G
 
