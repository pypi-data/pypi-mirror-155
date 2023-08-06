class SendMessage:
    def __init__(self, connection_object):
        self.connection_object = connection_object

    def wait_heartbeat(self):
        self.connection_object.wait_heartbeat()

    def send_cmd(self, command, p1, p2, p3, p4, p5, p6, p7, target_sysid=None, target_compid=None):
        """Send a MAVLink command long."""
        self.connection_object.mav.command_long_send(target_sysid, target_compid, command, 1,  # confirmation
                                                     p1, p2, p3, p4, p5, p6, p7)

    def run_cmd_get_ack(self, command, want_result, timeout, quiet=False):
        # start = get_sim_time_cached()
        while True:
            # delta_time = get_sim_time_cached() - start
            # if delta_time > timeout:
            #    raise AutoTestTimeoutException("Did not get good COMMAND_ACK within %fs" % timeout)
            #    print('ERROR', "Did not get good COMMAND_ACK within %fs" % timeout)
            m = self.connection_object.recv_match(type='COMMAND_ACK',
                                                  blocking=True,
                                                  timeout=0.1)
            if m is None:
                continue
            if not quiet:
                print("ACK received: %s" % (str(m)))
            if m.command == command:
                break
