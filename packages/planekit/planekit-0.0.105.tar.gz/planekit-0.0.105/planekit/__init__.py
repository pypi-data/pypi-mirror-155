from .main import print_hi
from .pymavlink import  mavutil
def a(str):
    print("hi")
    master = mavutil.mavlink_connection(str)
    # Wait a heartbeat before sending commands
    master.wait_heartbeat()
    # Choose a mode
