from . import backUpVals, restoreMethods


def restoreEpics(bak=backUpVals):
    print('Restoring channel values...')
    for ii in range(len(bak)-1, -1, -1):
        for ele in bak.values():
            if ii == ele['sno']:
                restoreMethods[ele['type']](ele)
