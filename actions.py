"""
    @author Leonardo Rossi Leão
    @create february, 02, 2022

    This file contains functions with actions 
    that are used in many parts of the code
"""

import os
from datetime import datetime

class Actions():

    # Get the current date and time
    @staticmethod
    def getDatetime():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    # Write something in a file with datetime control
    @staticmethod
    def recordAction(text, filename):
        file = open(filename, "a")
        file.write(f"[{Actions.getDatetime()}] {text} \n")
        file.close()

    # Get a file size
    @staticmethod
    def filesize(filename):
        stats = os.stat(filename)
        return stats.st_size