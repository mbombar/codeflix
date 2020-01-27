import api

def testusefulness():
    assert(api.isuseful('1280'))
    assert(not api.isuseful('409'))
    assert(api.isuseful('412'))
    contestslist = api.getcontestslist()
    assert(len(contestslist) == 2)
    contestsids = api.getcontestidslist(contestslist)
    assert(len(contestsids) == 0)

testusefulness()

