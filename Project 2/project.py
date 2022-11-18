"""
main file that invokes all the necessary procedures from these three files.
"""

import interface
from preprocessing import *

if __name__ == '__main__':
    metadata = interface.GUI().initialise_GUI()
    if(metadata != None):
        host, port, database, username, password = metadata
        connect = ConnectAndQuery(host, port, database, username, password)
        interface.GUI().main_window(connect)
    