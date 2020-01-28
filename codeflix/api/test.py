import api


def testusefulness():
    try:
        print('Testing isuseful')
        assert(api.isuseful('1280'))
        assert(not api.isuseful('409'))
        assert(api.isuseful('412'))
        print('Testing getcontestslist')
        contestslist = api.getcontestslist()
        assert(contestslist)
        print('Testing getcontestidslist')
        contestsids = api.getcontestidslist(contestslist)
        assert(len(contestsids) == len(contestslist))
        print('Testing filterusefulcontests')
        usefulids = api.filterusefulcontests(contestsids)
        assert(len(usefulids) == 1069)
        print('Testing passed !')
    except AssertionError:
        print('Error !')


testusefulness()
