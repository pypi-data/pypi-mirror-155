from planekit.Data.Imu import Imu
from planekit.Data.Gps import Gps


class ReceiveData:
    def __init__(self, connection_object):
        self.connection_object = connection_object
        self.imu_message = None
        self.gps_message = None

    def get_message_object(self):
        return self.connection_object.recv_match()

    def select_imu_message(self):
        while True:
            self.imu_message = ReceiveData(self.connection_object).get_message_object()
            if self.imu_message is not None and self.imu_message.get_type() == 'RAW_IMU':
                imu_message = Imu(self.imu_message)
                return imu_message

    def select_gps_message(self):
        while True:
            self.gps_message = ReceiveData(self.connection_object).get_message_object()
            if self.gps_message is not None and self.gps_message.get_type() == 'GPS_RAW_INT':
                gps_message = Gps(self.gps_message)
                return gps_message

    def ground_speed_message(self):
        while True:
            self.gps_message = ReceiveData(self.connection_object).get_message_object()
            if self.gps_message is not None and self.gps_message.get_type() == 'GPS_RAW_INT':
                gps_message = Gps(self.gps_message)
                return gps_message.vel
