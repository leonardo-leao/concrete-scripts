"""
    @author Leonardo Rossi Leão
    @create february, 02, 2022

    These scripts process the data got by
    GeoLogger G8 and sensors of temperature and
    deformation
"""

# coding=utf-8

# Libraries
import os
import time
import threading
import pandas as pd
from epics import EpicsServer
from actions import Actions as act
from calibration import Calibration

class Processing(threading.Thread):

    # Constructor Method
    def __init__(self):

        # Initialize the thread 
        super(Processing, self).__init__()
        self.kill = threading.Event()

        # FTP directory
        self.ftp_directory = "/usr/data/ftp-concrete/"

        # Initialize the Epics server
        self.server = EpicsServer()
        self.server.start()

    # Convert received data and set to Epics
    def fileManipulation(self, directory, filename):

        position = 0
        rawData = pd.read_csv(directory + filename)
        
        # Get Mux ID from the file
        muxID = int(filename.replace("DT", "").replace(".CSV", "").replace(".csv", ""))

        # Get the last updated data from the file
        lastData = rawData.tail(1).values[0][0].split(";|;")

        # Append the lastest data in muxData list
        for value in lastData:
            for subvalue in value.split(";"):
                if position >= 3:
                    channel, converted = Calibration.convert(muxID, position, subvalue)
                    print(f"{channel}: {converted}")
                    self.server.update(muxID, (position // 2) + 1, position % 2, converted)
                position += 1

    def run(self):

        act.recordAction("File monitor was started", "monitor.txt")

        # Create a dictionary with the filenames and theirs sizes
        filesToWatch = {}
        for filename in os.listdir(self.ftp_directory):
            if "DT" in filename:
                filesToWatch[filename] = act.filesize(self.ftp_directory + filename)

        # Running while Thread is not kill
        while not self.kill.is_set():

            # Error prevention
            for filename in filesToWatch:
                currentSize = act.filesize(self.ftp_directory + filename)
                if currentSize != filesToWatch[filename]:
                    act.recordAction(f"Size changed in {filename}: {filesToWatch[filename]} kb -> {currentSize} kb", "monitor.txt")
                    filesToWatch[filename] = currentSize
                    self.fileManipulation(self.ftp_directory, filename)

            # Set a delay to reanalyse
            time.sleep(1)

    # Stop the thread        
    def stop(self):
        act.recordAction("Stop file monitor", "monitor.txt")
        self.kill.set()
        
if __name__ == "__main__":
    thread = Processing()
    thread.start()
