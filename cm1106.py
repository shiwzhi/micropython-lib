from time import sleep

class CM1106:
    def __init__(self, uart) -> None:
        self.uart = uart

    def set_uart(self, uart):
        self.uart = uart

    def get_co2(self):
        try:
            co2_command = [0x11, 0x01, 0x01]
            co2_command.append(self.cal_crc(co2_command))
            self.uart.write(bytes(co2_command))
            sleep(0.5)
            response = list(self.uart.read(8))
            co2 = response[3]*256+response[4]
            return co2
        except:
            return 0

    # day 1-30
    def setABC(self, day):
        abc_command = [0x11, 0x7, 0x10, 0x64, 0x0, int(day), 0x1, 0x90, 0x64]
        abc_command.append(self.cal_crc(abc_command))
        self.uart.write(bytes(abc_command))
        sleep(0.3)
        response = self.uart.read(50)
        if response:
            print(f"abc response: {response}")

    def closeABC(self):
        close_abc_command = [0x11, 0x7, 0x10, 0x64, 0x2, 0x1, 0x1, 0x90, 0x64]
        close_abc_command.append(self.cal_crc(close_abc_command))
        self.uart.write(bytes(close_abc_command))
        sleep(0.3)
        response = self.uart.read(50)
        if response:
            print(f"close abc response: {response}")

    def cal_sensor(self, co2):
        h_byte = co2//256
        l_byte = co2 - (h_byte*256)
        calibrate_command = [0x11, 0x03, 0x03, h_byte, l_byte] # calibrate co2 to 1*256+0x90 400
        calibrate_command.append(self.cal_crc(calibrate_command))
        print(f"cal_command: {calibrate_command}")
        self.uart.write(bytes(calibrate_command))
        sleep(0.3)
        response = self.uart.read(50)
        if response:
            print(f"calibrate co2 response: {response}")

    def cal_crc(self, data):
        crc = 0
        for i in data:
            crc += i
        crc = 256 - (crc % 256)
        return crc