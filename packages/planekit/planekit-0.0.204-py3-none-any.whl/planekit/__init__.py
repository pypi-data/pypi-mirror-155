from planekit.mavlink.Connection import Connection as MavLinkConnection
from planekit.mavlink.SendMessage import SendMessage
from planekit.Data.Imu import Imu
from planekit.mavlink.ReceiveData import ReceiveData


class Connection:
    def __init__(self, connection_string):
        self.mavlink = MavLinkConnection()
        # master
        self.connection_object = self.mavlink.connection(connection_string)
        self.connection_string = connection_string

    def wait_heartbeat(self):
        m = SendMessage(self.connection_object)
        m.wait_heartbeat()

    # Test remove prod.
    def get_connection(self):
        self.mavlink.get_connection()

    def imu_message(self):
        return ReceiveData(self.connection_object).select_imu_message()

    def gps_message(self):
        return ReceiveData(self.connection_object).select_gps_message()

    def ground_speed(self):
        return ReceiveData(self.connection_object).ground_speed_message()
