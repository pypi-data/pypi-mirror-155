import epics
from . import backUpVals, restoreMethods
from time import sleep


def caput(pvname, value, wait=False, timeout=60.0, bak=backUpVals, tramp=None):
    val = epics.caget(pvname, timeout=timeout)
    if pvname not in bak:
        bak[pvname] = {'type': 'channel', 'value': val, 'tramp': tramp,
                       'sno': len(bak), 'name': pvname}
    if tramp is None:
        epics.caput(pvname=pvname, value=value, wait=wait, timeout=timeout)
    else:
        rampYourself = True
        # If this looks like a GAIN channel, look for TRAMP channel
        if pvname[-4:] == 'GAIN':
            try:
                trch = pvname[:-4] + 'TRAMP'
                tbak = epics.caget(pvname=trch, timeout=timeout)
                rampYourself = False
            except BaseException:
                rampYourself = True
        if not rampYourself:
            epics.caput(pvname=trch, value=tramp, wait=wait, timeout=timeout)
            epics.caput(pvname=pvname, value=value, wait=wait, timeout=timeout)
            sleep(tramp)
            epics.caput(pvname=trch, value=tbak, wait=wait, timeout=timeout)
        else:
            rampSteps = 100
            valStep = (value - val) / rampSteps
            for tstep in range(1, rampSteps):
                epics.caput(pvname=pvname, value=val + valStep * tstep,
                            wait=wait, timeout=timeout)
                sleep(tramp / rampSteps)
            epics.caput(pvname=pvname, value=value, wait=wait, timeout=timeout)


def restoreChannel(bakVal):
    epics.caput(bakVal['name'], bakVal['value'])


restoreMethods['channel'] = restoreChannel
