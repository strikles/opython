import OpenHoldem
import math

class Main:
    gotcaught = False
    ibluffed = False
    inv = -1
    phr = -1
    oh = {
        'betround': -1,
        'handrank169': -1,
        'prwin': -1,
        'prtie': -1,
        'prlos': -1,
        'nplayersplaying': -1,
        'call': -1,
        'currentbet': -1,
        'balance': -1,
        'pot': -1,
        'bblind': -1,
        'didfold': -1,
        'didchec': -1,
        'didcall': -1,
        'didrais': -1,
        'didbetsize': -1,
        'didalli': -1
    }

    def __init__(self):
        self.gotcaught = False
        self.ibluffed = False
        self.inv = 0
        self.phr = 0
        for k, v in self.oh.items():
            self.oh[k] = 0

    def updateVars(self):
        print('---------------------\n')
        for k, v in self.oh.items():
            self.oh[k] = OpenHoldem.getSymbol(k)
            print(f'{k}: {self.oh[k]}\n')
        self.phr = (170.0 - self.oh['handrank169'])/169.0
        self.inv = 1.0/self.oh["nplayersplaying"]
        print(f'1/nplayers: {self.inv}\n')
        if self.oh["betround"] == 1:
            self.gotcaught = False
            self.ibluffed = False
        if self.oh["betround"] > 1 and self.timesActed() > 0 and self.ibluffed == True:
            self.gotcaught = True

    def timesActed(self):
        return int(self.oh["didfold"] + self.oh["didchec"] + self.oh["didcall"] + self.oh["didrais"] + self.oh["didbetsize"])

    def callExpectedValue(self):
        ev = self.oh["prwin"]*self.oh["pot"] + self.oh["prtie"]*self.inv*self.oh["pot"] - self.oh["prlos"]*self.oh["call"]
        print(f'ev: {ev}\n')
        return ev

    def preFlopDecision(self):
        decision = 0.0
        print(f'phr: {self.phr}\n')
        if 0.95 < self.phr:
            if self.timesActed() == 0:
                decision = OpenHoldem.getSymbol("RaiseHalfPot")
            else:
                decision = OpenHoldem.getSymbol("RaiseMax")
            print('-> 0.95\n')
        elif 0.85 < self.phr and self.oh["call"] <= 13.0*self.oh["bblind"]:
            if self.timesActed() == 0:
                decision = OpenHoldem.getSymbol("RaiseHalfPot")
            else:
                decision = OpenHoldem.getSymbol("Call")
            print('-> 0.85\n')
        elif 0.70 < self.phr and self.oh["call"] <= 3.0*self.oh["bblind"]:
            if self.timesActed() == 0:
                decision = OpenHoldem.getSymbol("Call")
            print('-> 0.70\n')
        return decision

    def postFlopDecision(self):
        decision = 0.0
        min_bet = max(2.0*self.oh["call"], self.oh["bblind"])
        if 0.40 < self.oh["prwin"] - self.inv:
            if self.timesActed() == 0:
                decision = OpenHoldem.getSymbol("RaisePot")
            else:
                decision = OpenHoldem.getSymbol("RaiseMax")
        elif 0.1 < self.oh["prwin"] - self.inv and math.isclose(0, self.oh["call"], rel_tol=1e-6) and self.gotcaught == False:
            decision = OpenHoldem.getSymbol("RaiseHalfPot")
            self.ibluffed = True
        elif self.oh["call"] < self.callExpectedValue():
            decision = OpenHoldem.getSymbol("Call")
        return decision

    def getDecision(self):
        decision = 0.0
        self.updateVars()
        if self.oh["betround"] == 1:
            if self.oh["prwin"] > self.inv:
                decision = self.preFlopDecision()
        else:
            decision = self.postFlopDecision()
        print(f'decision: {decision}\n')
        return decision