import traceback
from enum import Enum
from _bleio.exceptions import BluetoothError
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from bleak.exc import BleakError


class VibrotactorArrayCommands(Enum):
    WRITE_MOTOR_LEVEL = 0x01
    SET_MOTOR_LEVEL = 0x02
    TRIGGER_VIB = 0x03
    START_IMU = 0x04
    GET_SIDE = 0x05
    SET_FREQUENCY = 0x06
    STOP_IMU = 0x07


class VibrotactorArraySide(Enum):
    LEFT = b'\x01'
    RIGHT = b'\x00'


class VibrotactorArrayReturn(Enum):
    PASS = b'\x00'
    FAIL = b'\x01'
    ERROR = -1


class VibrotactorArrayData(Enum):
    AX = 0
    AY = 1
    AZ = 2
    GX = 3
    GY = 4
    GZ = 5
    MX = 6
    MY = 7
    MZ = 8
    HEADING = 9
    PITCH = 10
    ROLL = 11


class VibrotactorArray:
    def __init__(self, ble, motor_count=12, max_vib=255):
        self.motor_count = motor_count
        self.max_vib = max_vib
        self.uart_connection = None
        self.uart_service = None
        self.ble = ble
        self.streaming = False
        if self.connect():
            print("INFO: Vibrotactor array connected!")
        else:
            print("INFO: Vibrotactor array not found!")

    def connect(self):
        self.uart_connection = None
        for tries in range(0, 10):
            if not self.uart_connection:
                try:
                    for adv in self.ble.start_scan(ProvideServicesAdvertisement):
                        if UARTService in adv.services:
                            self.uart_connection = self.ble.connect(adv)
                            break
                    self.ble.stop_scan()
                except BluetoothError:
                    pass
                except BleakError:
                    pass
        if self.uart_connection and self.uart_connection.connected:
            self.uart_service = self.uart_connection[UARTService]
            return True
        else:
            return False

    def write_all_motors(self, vib_strength):
        for i in range(0, self.motor_count):
            self.write_motor_level(i, vib_strength)

    def write_motor_level(self, motor_index, vib_strength):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            if 0 <= motor_index < self.motor_count:
                if 0 <= vib_strength <= self.max_vib:
                    write_motor_command = bytearray([VibrotactorArrayCommands.WRITE_MOTOR_LEVEL.value, motor_index, vib_strength])
                    self.uart_service.write(write_motor_command)
                else:
                    return False
            else:
                return False
        else:
            return False

    def set_all_motors(self, vib_strength):
        for i in range(0, self.motor_count):
            self.set_motor_level(i, vib_strength)

    def set_motor_level(self, motor_index, vib_strength):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            if 0 <= motor_index < self.motor_count:
                if 0 <= vib_strength <= self.max_vib:
                    write_motor_command = bytearray([VibrotactorArrayCommands.SET_MOTOR_LEVEL.value, motor_index, vib_strength])
                    self.uart_service.write(write_motor_command)
                else:
                    return False
            else:
                return False
        else:
            return False

    def trigger_vib(self):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            write_motor_command = bytearray([VibrotactorArrayCommands.TRIGGER_VIB.value, 0, 0])
            self.uart_service.write(write_motor_command)
        else:
            return False

    def start_imu(self):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            write_motor_command = bytearray([VibrotactorArrayCommands.START_IMU.value, 0, 0])
            self.uart_service.write(write_motor_command)
            return_bytes = self.uart_service.read(1)
            try:
                return_code = VibrotactorArrayReturn(return_bytes)
                if return_code == VibrotactorArrayReturn.FAIL:
                    return return_code
                self.streaming = True
                return return_code
            except ValueError:
                return VibrotactorArrayReturn.ERROR
        else:
            return False

    def stop_imu(self):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            command = bytearray([VibrotactorArrayCommands.STOP_IMU.value, 0, 0])
            self.uart_service.write(command)
            return_bytes = self.uart_service.read(1)
            try:
                return_code = VibrotactorArrayReturn(return_bytes)
                if return_code == VibrotactorArrayReturn.FAIL:
                    return return_code
                self.streaming = False
                return return_code
            except ValueError:
                return VibrotactorArrayReturn.ERROR
        else:
            return False

    def get_side(self):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            write_motor_command = bytearray([VibrotactorArrayCommands.GET_SIDE.value, 0, 0])
            self.uart_service.write(write_motor_command)
            return_bytes = self.uart_service.read(1)
            try:
                return VibrotactorArraySide(return_bytes)
            except ValueError:
                return VibrotactorArrayReturn.ERROR
        else:
            return False

    def set_motor_frequency(self, freq_select):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            set_freq_command = bytearray([VibrotactorArrayCommands.SET_FREQUENCY.value, freq_select, 0])
            self.uart_service.write(set_freq_command)
            return_bytes = self.uart_service.read(1)
            try:
                return VibrotactorArraySide(return_bytes)
            except ValueError:
                return VibrotactorArrayReturn.ERROR

    @staticmethod
    def get_ble_instance():
        return BLERadio()
