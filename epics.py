"""
    @author Leonardo Rossi Leão
    @create february, 02, 2022
"""

import threading
from actions import Actions as act
from pcaspy import SimpleServer, Driver
from pv import PvProperties as pvp

class EpicsDriver(Driver):

    # Initialize the Epics driver
    def _init_(self):
        super(EpicsDriver, self)._init_()

    # Function responsible for writing in the PV
    def write(self, reason, value):
        self.setParam(reason, value)

    # Function responsible for reading PV data
    def read(self, reason):
        return self.getParam(reason)

class EpicsServer(threading.Thread):
    
    driver = None           # Contains the epics driver
    updateMonitor = {}      # Stores the time of the last pv update
    
    # Initialize the Epics server
    def _init_(self):
        super(EpicsServer, self)._init_()

    # Update PV data
    def update(mux, channel, subchannel, value):
        subchannel = "A" if subchannel == 0 else "B"
        pv = pvp.pvName(mux, channel, subchannel)
        if pv != "Dis.":
            EpicsServer.driver.write(pv, value)
            EpicsServer.updateMonitor[pv] = act.getDatetime()
        else:
            act.recordAction("PV is disable", "epicsMonitor.txt")        
        
    def run(self):
        server = SimpleServer()
        server.createPV("TU-", pvp.pvdb())
        EpicsServer.driver = EpicsDriver()
        act.recordAction("EPICS server and driver was started", "rawMonitor.txt")
        while True:
            server.process(0.1)