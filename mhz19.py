import uasyncio as asyncio
from time import sleep


class MHZ19:
    def __init__(self, uart) -> None:
        self.uart = uart

    def set_uart(self, uart):
        self.uart = uart

    def get_co2(self):
        co2_command = [0XFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]
        self.uart.write(bytes(co2_command))
        sleep(0.5)
        response = self.uart.read(9)
        if not response:
            return None
        a = list(response)
        print(a)
        checksum = 0
        for i in range(1, 7):
            checksum += a[i]
        checksum %= 256
        checksum = ~checksum & 0xFF
        checksum += 1
        print(f"checksum: {checksum}")
        co2 = a[2]*256+a[3]
        return co2
