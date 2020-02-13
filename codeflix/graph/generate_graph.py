import sys

if '../' not in sys.path:
    sys.path.append('../')

from api import api  # noqa: E402
import networkx as nx  # noqa: E402


def add_edge(user, problem, solved, g):
    if solved or not g.has_edge(user, problem):
        g.add_edge(user, problem, weight=(0 if solved else 1))


def add_contest(contestid, g, users_set, pbs_set):
    (solves, users, pbs) = api.solvedsubmissionsduringcontest(contestid)
    for pb in pbs:
        pbs_set.add(pb)
    for user in users:
        users_set.add(user)
        for pb in pbs:
            add_edge(user, pb, False, g)
    for (user, pb) in solves:
        add_edge(user, pb, True, g)


def create_graph_from_ids(contestids, verbose=True):
    g = nx.Graph()
    users = set()
    problems = set()
    for contestid in contestids:
        if verbose:
            # USED FOR TESTING
            print('NEW CONTEST ' + str(contestid))
        add_contest(contestid, g, users, problems)
    return (g, users, problems)


def create_graph(check=True, verbose=True):
    contestslist = api.getcontestslist(check)
    contestsids = api.getcontestidslist(contestslist)
    usefulids = api.filterusefulcontests(contestsids, check)
    return create_graph_from_ids(usefulids, verbose)
