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
        request = http.request('GET', 'http://codeforces.com/api/{}'.format(req))
        return json.loads(request.data)


# Get the list of all contests.
def getcontestslist():
    try:
        return makecfrequest('contest.list?gym=false')
    except:
        print('FAIL')
        return None

# From a list of contests, get the list of corresponding ids.
# TO DEBUG
def getcontestidslist(contestslist):
    return []
    #return list(map(lambda c: print(c), c['id'], list(contestslist)))

# From a contest id, decide if we should take it into account.
def isuseful(contestid):
    try:
        l = makecfrequest('contest.ratingChanges?contestId={}'.format(contestid))
        return l['status'] == 'OK'
    except:
        print('FAIL')
        return False

# From a list of contest ids.
def filterusefulcontests(contestsidlist):
    return list(filter(isuseful, contestsidlist))

# Get the list of submissions in a contest.
def getsubmissionslist(contestid):
    try:
        return makecfrequest('contest.status?contestId={}'.format(contestid))
    except:
        print('FAIL')
        return None

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
