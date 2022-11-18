"""
main file that invokes all the necessary procedures from these three files.
"""

import interface
from preprocessing import *

if __name__ == '__main__':
    connectMetadata = interface.GUI().initialise_GUI()
    if connectMetadata is not None:
        host, port, database, username, password = connectMetadata
        SQL_connect = ConnectAndQuery(host, port, database, username, password)
        interface.GUI().main_window(SQL_connect)
    