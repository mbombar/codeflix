import sys
import socket
import string
import urllib3
import datetime
import time
import select
import fcntl, os
from socket import AF_INET, SOCK_DGRAM
import json

# Make a codeforces request.
def makecfrequest(req):
    http = urllib3.PoolManager()
    request = http.request('GET', 'https://codeforces.com/api/{}'.format(req))
    time.sleep(0.21) # Codeforces api limits to 5 requests per second.
    return json.loads(request.data)


# Get the list of all contests.
def getcontestslist():
    return makecfrequest('contest.list?gym=false')


def getcontest(contestslist, contestid):
        """
        get contest object with id `contestid` from the contestslist
        """
        return list(filter(lambda c: c['id'] == contestid, contestslist))[0]

# From a list of contests, get the list of corresponding ids.
# TO DEBUG
def getcontestidslist(contestslist):
    """
    contestslist is a list of contests, eg getcontestslist['result']
    """
    return list(map(lambda c: c['id'], contestslist))


def getRatingInfo(contestid):
        return makecfrequest('contest.ratingChanges?contestId={}'.format(contestid))



# From a contest id, decide if we should take it into account.
def isuseful(contestid):
    l = makecfrequest('contest.ratingChanges?contestId={}'.format(contestid))
    return l['status'] == 'OK'


# From a list of contest ids.
def filterusefulcontests(contestsidlist):
    return list(filter(isuseful, contestsidlist))

# Get the list of submissions in a contest.
def getsubmissionslist(contestid):
    return makecfrequest('contest.status?contestId={}'.format(contestid))

# Extract only solved submissions in a list of submissions.
def solvedsubmissions(listsubmissions):
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
