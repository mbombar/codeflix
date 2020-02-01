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


from codeforces.models import Attempt, CodeforcesUser, Contest, Problem, ProblemTag
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

def getcontest(contestid):
    """
    Get contest object with id `contestid` from the contestslist
    """
    try:
        contest = Contest.objects.get(id=contestid)
    except Contest.DoesNotExist:
        contestlist = getcontestlist()
        contest = list(filter(lambda c: c['id'] == int(contestid), contestslist))[0]
        date = dict_camel_to_snake(contest)
        contest = Contest(**data)
        contest.save()
    return contest

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
    contest = getcontest(contestid)
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

def getusersubmissions(handle):
    """
    Get the list of submissions for a given user.
    """
    response = makecfrequest('user.status?handle={}'.format(handle))
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
    """
    contest = getcontest(contestid)
    attempts = contest.attempt_set.all()

    if attempts.count() == 0:
        r = makecfrequest('contest.standings?contestId={}'.format(contestid))
        request = handleresponse(r)
        pbs = request['problems']

        for pb in pbs:
            obj = store_pb(pb)
            contest.problems.add(obj)

        rows = request['rows']

        solves = []
        participants = []
        problems = list(map(lambda p : p['name'], pbs))

        for ranklistrow in rows:
            if ranklistrow['party']['participantType'] != 'CONTESTANT':
                continue
            for member in ranklistrow['party']['members']:
                user = member['handle']
                try:
                    cfuser = CodeforcesUser.objects.get(handle=user)
                except CodeforcesUser.DoesNotExist:
                    data = getusers([user])
                    data = exctractuserinfo(data)
                    cfuser = CodeforcesUser(**data)
                    cfuser.save()
                participants.append(user)
                for i, pb in enumerate(problems):
                    problem = Problem.objects.get(name=pb)
                    pbresult = ranklistrow['problemResults'][i]
                    if pbresult.get('bestSubmissionTimeSeconds'):
                        solved=True
                        solves.append((user, problem.name))
                    else:
                        solved=False
                    a = Attempt(contest=contest, problem=problem, author=cfuser, solved=solved)
                    a.save()
        return (solves, participants, problems)

    else:
        solves = list(map(lambda d: tuple(d.values()), attempts.filter(solved=True).values("author__handle", "problem__name")))
        participants = set()
        for x in map(lambda d: set(d.values()), attempts.values("author__handle")):
            participants.update(x)
        problems = list(map(lambda p : p.name, contest.problems.all()))
        return (solves, list(participants), problems)

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

def extractuserinfo(user):
    """
    Extract user info to be stored inside the database.
    """
    data = {key: user[key] for key in ["handle", "firstName", "lastName"]}
    return dict_camel_to_snake(data)

def store(user):
    """
    Create a database object representing the user in argument
    """
    cfuser = extractuserinfo(user)
    obj, created = CodeforcesUser.objects.get_or_create(**cfuser)

def store_pb(problem):
    """
    Create a database object reprensenting the problem in argument
    """
    pb = dict_camel_to_snake(problem)
    tags = pb.pop('tags')
    tags_obj = []
    pb_obj, created = Problem.objects.get_or_create(**pb)
    for tag in tags:
        tag_obj, tag_created = ProblemTag.objects.get_or_create(name=tag)
        tags_obj.append(tag_obj)
    for tag in tags_obj:
        pb_obj.tags.add(tag)
        pb_obj.save()
    return pb_obj
