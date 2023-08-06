from time import sleep
from epics import caget
from .caput import caput
from . import backUpVals, restoreMethods


def writeChannels(chanInfo, bak=backUpVals):
    '''
    Write epics channels given in a dictionary format together.
    '''
    # Allowing to write the value directly under channel names if no other
    # parameter is required.
    for ch in chanInfo['channels']:
        if not isinstance(chanInfo['channels'][ch], dict):
            chanInfo['channels'][ch] = {'value': chanInfo['channels'][ch]}
        else:
            if 'value' not in chanInfo['channels'][ch]:
                raise RuntimeError('No value found for ' + ch)

    discardBak = []  # caput used in this function do not need to save backUps
    kwargs = {'bak': discardBak}
    for ch in chanInfo['channels']:
        for arg in ['wait', 'timeout']:
            kwargs[ch] = {}
            if arg in chanInfo:  # If present as global argument
                kwargs[ch][arg] = chanInfo[arg]
            elif arg in chanInfo['channels'][ch]:
                kwargs[ch][arg] = chanInfo['channels'][ch][arg]

    curVals = {}
    for arg in ['tramp', 'wait', 'timeout']:
        if arg in chanInfo:
            curVals[arg] = chanInfo[arg]
    curVals['channels'] = {}
    for ch in chanInfo['channels']:
        curVals['channels'][ch] = {}
        for key in chanInfo['channels'][ch]:
            if key == 'value':
                curVals['channels'][ch][key] = caget(ch)
            else:
                curVals['channels'][ch][key] = chanInfo['channels'][ch][key]
    if all([set(curVals['channels']) != set(ele['value']['channels'])
            for ele in bak.items() if ele['type'] == 'group']):
        name = 'group_of|' + '|'.join(list(curVals['channels'].keys()))
        bak[name] = [{'type': 'group', 'value': curVals, 'sno': len(bak)}]

    rampYourself = True
    if 'tramp' in chanInfo:
        oldTramps = {}
        if chanInfo['tramp'] > 0:
            for ch in chanInfo['channels']:
                fus = ch.rfind('_') + 1
                if ch[fus:] in ['GAIN', 'OFFSET']:
                    try:
                        trampCh = ch[:fus] + 'TRAMP'
                        oldTramps[trampCh] = caget(trampCh)
                        rampYourself = rampYourself and False
                    except BaseException:
                        rampYourself = rampYourself or True
                else:
                    rampYourself = rampYourself or True
            if rampYourself:
                for ch in oldTramps:
                    caput(ch, 0, bak=discardBak)
                rampSteps = 100
                sleepTime = chanInfo['tramp'] / rampSteps
                curVals = {}
                for ch in chanInfo['channels']:
                    curVals[ch] = caget(ch)
                stepVals = {}
                for ch in curVals:
                    stepVals[ch] = (chanInfo['channels'][ch]['value']
                                    - curVals[ch]) / rampSteps
                for tstep in range(1, rampSteps):
                    sleep(sleepTime)
                    for ch in chanInfo['channels']:
                        caput(ch, curVals[ch] + tstep * stepVals[ch],
                              **kwargs[ch])
            else:
                for ch in oldTramps:
                    caput(ch, chanInfo['tramp'], bak=discardBak)
        # Write final values
        for ch in chanInfo['channels']:
            caput(ch, chanInfo['channels'][ch]['value'], **kwargs[ch])
        if not rampYourself:
            sleep(chanInfo['tramp'])
        sleep(0.1)  # Buffer time
        for ch in oldTramps:
            caput(ch, oldTramps[ch], bak=discardBak)
    else:
        for ch in chanInfo['channels']:
            if 'tramp' in chanInfo['channels'][ch]:
                kwargs[ch]['tramp'] = chanInfo['channels'][ch]['tramp']
            caput(ch, chanInfo['channels'][ch]['value'], **kwargs[ch])


def restoreGroup(bakVal):
    writeChannels(chanInfo=bakVal['value'], bak=[])


restoreMethods['group'] = restoreGroup
