"""
    @author Leonardo Rossi Leão
    @create february, 02, 2022
    @update april, 07, 2022
"""

import json
import threading
from actions import Actions as act
from pcaspy import SimpleServer, Driver
from pv import PvProperties as pvp

class EpicsDriver(Driver):

    # Initialize the Epics driver
    def __init__(self):
        super(EpicsDriver, self).__init__()

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
    def update(self, mux, channel, subchannel, value):
        pv = pvp.pvName(mux, channel, subchannel)
        if pv not in ["Dis.", ""] and value != "Dis.":
            EpicsServer.driver.write(pv.replace("TU-", ""), value)
            EpicsServer.updateMonitor[pv] = act.getDatetime()

            # Update the monitoring file of pv update
            with open("pvMonitor.txt", 'w') as f: 
                for key, value in sorted(EpicsServer.updateMonitor.items()): 
                    f.write('TU-%s: %s\n' % (key, value))
    
        else:
            act.recordAction(f"PV of channel {channel}{subchannel} is disable", "epicsMonitor.txt")        
        
    def run(self):
        server = SimpleServer()
        server.createPV("TU-", pvp.pvdb())
        EpicsServer.driver = EpicsDriver()
        act.recordAction("EPICS server and driver was started", "epicsMonitor.txt")
        while True:
            server.process(0.1)