import json
import os
import sys
import time

import django
import urllib3

if '../' not in sys.path:
    sys.path.append('../')

# Setup django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codeflix.settings')
django.setup()


from codeforces.models import Contest, CodeforcesUser
from utils import dict_camel_to_snake

class CodeforcesIssue(Exception):
    """
    Basic error raised when something got wrong using the API
    """
    def __init__(self, msg=""):
        Exception.__init__(self, msg)

def makecfrequest(req):
    """
    Make a codeforces request.
    """
    http = urllib3.PoolManager()
    request = http.request('GET', 'https://codeforces.com/api/{}'.format(req))
    time.sleep(0.21)  # Codeforces api limits to 5 requests per second.
    return json.loads(request.data)


def handleresponse(response):
    """
    Handle a response of a codeforces request.
    If something has gone wrong, raise CodeforcesIssue exception.
    """
    status = response['status']
    if status == 'OK':
        try:
            return response['result']
        except KeyError:
            raise CodeforcesIssue('Status OK but I got no response')
    else:
        raise CodeforcesIssue(response.get('comment', 'Unknown Error'))



def getcontestslist():
    """
    Get the list of all contests.
    """
    response = makecfrequest('contest.list?gym=false')
    return handleresponse(response)


def getcontest(contestslist, contestid):
    """
    Get contest object with id `contestid` from the contestslist
    """
    return list(filter(lambda c: c['id'] == int(contestid), contestslist))[0]


def getcontestidslist(contestslist):
    """
    From a list of contests, get the list of corresponding ids.
    """
    return list(map(lambda c: c['id'], contestslist))


def getratinginfo(contestid):
    """
    Get rating info of contest of id `contestid`
    """
    response = makecfrequest('contest.ratingChanges?contestId={}'.format(contestid))
    return handleresponse(response)


def _isuseful(contestid, contests=None):
    """
    From a contest id, decide if we should take it into account.
    It first searches for the contest in the database, and insert it otherwise.

    Not meant to be applied directly
    """
    try:
        contest = Contest.objects.get(id=contestid)
        if contest.useful:
            # Once the contest has been marked at useful, it remains useful
            return True, contests
        else:
            # A contest might not be useful yet, so we check usefulness.
            req = makecfrequest('contest.ratingChanges?contestId={}'.format(contestid))
            useful = req['status'] == 'OK'
            contest.useful = useful
            contest.save()
            return useful, contests
    except Contest.DoesNotExist:
        if not contests:
            contests = getcontestslist()
        contest = getcontest(contests, contestid)
        req = makecfrequest('contest.ratingChanges?contestId={}'.format(contestid))
        useful = req['status'] == 'OK'
        data = dict_camel_to_snake(contest)
        data['useful'] = useful
        obj = Contest(**data)
        obj.save()
        return useful, contests

def isuseful(contestid):
    """
    From a contest id, decide if we should take it into account.
    It first searches for the contest in the database, and insert it otherwise.
    """
    return _isuseful(contestid)[0]

def filterusefulcontests(contestsidlist):
    """
    Get all useful contests from a list of contest ids
    """
    return list(filter(isuseful, contestsidlist))


def getsubmissionslist(contestid):
    """
    Get the list of submissions in a contest.
    """
    response = makecfrequest('contest.status?contestId={}'.format(contestid))
    return handleresponse(response)


def solvedsubmissions(listsubmissions):
    """
    Extract solved submissions, participants and problem names
    in a list of submissions.
    """
    solves, participants, problems = set(), set(), set()
    for submi in listsubmissions:
        solvers_party = submi['author']
        solvers = solvers_party['members']
        solver = solvers[0]['handle']
        problem = submi['problem']['name']

        participants.add(solver)
        problems.add(problem)

        if submi['verdict'] == 'OK':
            solves.add((solver, problem))
    return (solves, participants, problems)

def solvedsubmissionsfromid(contestid):
    """
    Extract solved submissions, participants and problem names
    from a contest given its contest id.
    """
    listsubmissions = getsubmissionslist(contestid)
    return solvedsubmissions(listsubmissions)

def solvedsubmissionsduringcontest(contestid):
    """
    Extract solved submissions, participants and problem names
    **during** a contest given its contest id.
    TODO: Cache this.
    """
    r = makecfrequest('contest.standings?contestId={}'.format(contestid))
    request = r['result']
    pbs = request['problems']
    rows = request['rows']
    
    solves = []
    participants = []
    problems = list(map(lambda p : p['name'], pbs))
    nbproblems = len(problems)

    for ranklistrow in rows:
        if ranklistrow['party']['participantType'] != 'CONTESTANT':
            continue
        user = ranklistrow['party']['members'][0]['handle']
        participants.append(user)
        for i in range(nbproblems):
            pbresult = ranklistrow['problemResults'][i]
            if pbresult['type'] == 'FINAL':
                solves.append((user, problems[i]))
    return (solves, participants, problems)

def getratedusers(active=False):
    """
    Get the list of all rated users.
    If active, then only retrieve users who participated in rated contest during the last month.
    """
    response = makecfrequest('user.ratedList?activeOnly={}'.format(active))
    return handleresponse(response)


def getusers(handles=[]):
    """
    Get the specific users matching the handles in argument.
    `Handles` is a list of handles.
    Returns a list of User objects.
    """
    response = makecfrequest('user.info?handles={}'.format(";".join(handles)))
    return handleresponse(response)

def store(user):
    """
    Create a BDD object representing the user in argument
    """
    cfuser = dict_camel_to_snake(user)
    obj, created = CodeforcesUser.objects.get_or_create(**cfuser)
