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


from codeforces.models import Contest

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
            contest.useful = True
            contest.save()
            return useful, contests
    except Contest.DoesNotExist:
        if not contests:
            contests = getcontestslist()['result']
        contest = getcontest(contests, contestid)
        req = makecfrequest('contest.ratingChanges?contestId={}'.format(contestid))
        useful = req['status'] == 'OK'
        data = {}
        data['duration_seconds'] = contest.pop('durationSeconds')
        data['start_time_seconds'] = contest.pop('startTimeSeconds')
        data['relative_time_seconds'] = contest.pop('relativeTimeSeconds')
        data.update(contest)
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
