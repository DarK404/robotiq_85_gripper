import serial
from .gripper_io import GripperIO
from .modbus_crc import verify_modbus_rtu_crc
import array
import rclpy
import sys

class Robotiq85Gripper:
    def __init__(self,num_grippers=1,comport='/dev/ttyUSB0',baud=115200):

        try:
            self.ser = serial.Serial(comport,baud,timeout = 0.2)
        except:
            self.init_success = False
            return

        self._gripper = []
        self._num_grippers = num_grippers
        for i in range(self._num_grippers):
            self._gripper.append(GripperIO(i))
        self.init_success = True
        self._shutdown_driver = False

    def shutdown(self):
        self._shutdown_driver = True
        self.ser.close()

    def process_act_cmd(self,dev=0):
        if (dev >= self._num_grippers) or (self._shutdown_driver):
            return False
        try:
            self.ser.write(self._gripper[dev].act_cmd_bytes)
            #rclpy.loginfo('Act Cmd')
            #rclpy.loginfo(self._gripper[dev].act_cmd)
            rsp = self.ser.read(8)
            rsp = [int(x) for x in rsp]
            #rclpy.loginfo(rsp)
            if (len(rsp) != 8):
                #rclpy.logerr('Act Length is ' + str(len(rsp)))
                return False
            return verify_modbus_rtu_crc(rsp)
        except:
            #rclpy.logerr(sys.exc_info()[0])
            return False

    def process_stat_cmd(self,dev=0):
        try:
            self.ser.write(self._gripper[dev].stat_cmd_bytes)
            #rclpy.loginfo('Stat Cmd')
            #rclpy.loginfo(self._gripper[dev].stat_cmd)
            rsp = self.ser.read(21)
            rsp = [int(x) for x in rsp]
            #rclpy.loginfo(rsp)
            if (len(rsp) != 21):
                #rclpy.logerr('Stat Length is ' + str(len(rsp)))
                return False
            return self._gripper[dev].parse_rsp(rsp)
        except:
            #rclpy.logerr(sys.exc_info()[0])
            return False

    def activate_gripper(self,dev=0):
        if (dev >= self._num_grippers):
            return
        self._gripper[dev].activate_gripper()

    def deactivate_gripper(self,dev=0):
        if (dev >= self._num_grippers):
            return
        self._gripper[dev].deactivate_gripper()

    def activate_emergency_release(self,dev=0,open_gripper=True):
        if (dev >= self._num_grippers):
            return
        self._gripper[dev].activate_emergency_release(open_gripper)

    def deactivate_emergency_release(self,dev=0):
        if (dev >= self._num_grippers):
            return
        self._gripper[dev].deactivate_emergency_release()

    def goto(self, dev=0, pos=0.0, vel=1.0, force=1.0):
        if (dev >= self._num_grippers):
            return
        self._gripper[dev].goto(pos, vel, force)

    def stop(self,dev=0):
        if (dev >= self._num_grippers):
            return
        self._gripper[dev].stop()

    def is_ready(self,dev=0):
        if (dev >= self._num_grippers):
            return False
        return self._gripper[dev].is_ready()

    def is_reset(self,dev=0):
        if (dev >= self._num_grippers):
            return False
        return self._gripper[dev].is_reset()

    def is_moving(self,dev=0):
        if (dev >= self._num_grippers):
            return False
        return self._gripper[dev].is_moving()

    def is_stopped(self,dev=0):
        if (dev >= self._num_grippers):
            return False
        return self._gripper[dev].is_moving()

    def object_detected(self,dev=0):
        if (dev >= self._num_grippers):
            return False
        return self._gripper[dev].object_detected()

    def get_fault_status(self,dev=0):
        if (dev >= self._num_grippers):
            return 0
        return self._gripper[dev].get_fault_status()

    def get_pos(self,dev=0):
        if (dev >= self._num_grippers):
            return 0
        return self._gripper[dev].get_pos()

    def get_req_pos(self,dev=0):
        if (dev >= self._num_grippers):
            return 0
        return self._gripper[dev].get_req_pos()

    def get_current(self,dev=0):
        if (dev >= self._num_grippers):
            return 0
        return self._gripper[dev].get_current()