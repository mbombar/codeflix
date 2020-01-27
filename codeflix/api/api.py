import json
import time

import urllib3


def makecfrequest(req):
    """
    Make a codeforces request.
    """
    http = urllib3.PoolManager()
    request = http.request('GET', 'https://codeforces.com/api/{}'.format(req))
    time.sleep(0.21)  # Codeforces api limits to 5 requests per second.
    return json.loads(request.data)


def getcontestslist():
    """
    Get the list of all contests.
    """
    return makecfrequest('contest.list?gym=false')


def getcontest(contestslist, contestid):
    """
    Get contest object with id `contestid` from the contestslist
    """
    return list(filter(lambda c: c['id'] == contestid, contestslist))[0]


def getcontestidslist(contestslist):
    """
    From a list of contests, get the list of corresponding ids.
    contestslist is a list of contests, eg getcontestslist['result']
    """
    return list(map(lambda c: c['id'], contestslist))


def getratinginfo(contestid):
    """
    Get rating info of contest of id `contestid`
    """
    return makecfrequest('contest.ratingChanges?contestId={}'.format(contestid))


def isuseful(contestid):
    """
    From a contest id, decide if we should take it into account.
    """
    req = makecfrequest('contest.ratingChanges?contestId={}'.format(contestid))
    return req['status'] == 'OK'


def filterusefulcontests(contestsidlist):
    """
    Get all useful contests from a list of contest ids
    """
    return list(filter(isuseful, contestsidlist))


def getsubmissionslist(contestid):
    """
    Get the list of submissions in a contest.
    """
    return makecfrequest('contest.status?contestId={}'.format(contestid))


def solvedsubmissions(listsubmissions):
    """
    Extract only solved submissions in a list of submissions.
    """
    solves, participants, problems = [], [], []
    for submi in listsubmissions['result']:
        solvers_party = submi['author']
        solvers = solvers_party['members']
        solver = solvers[0]['handle']
        problem = submi['problem']['name']

        participants.append(solver)
        problems.append(problem)

        if submi['verdict'] == 'OK':
            solves.append((solver, problem))
    return (solves, participants, problems)
