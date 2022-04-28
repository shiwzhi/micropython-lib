import uasyncio as asyncio

class PMS:
    def __init__(self, uart) -> None:
        self.uart = uart
        self.passive_command = [0x42, 0x4D, 0xE1, 0x0, 0x0, 0x1, 0x70]
        self.read_command = [0x42, 0X4D, 0XE2, 0X0, 0X0, 0x1, 0x71]

    def set_uart(self, uart):
        self.uart = uart

    async def get_pms(self):
        self.uart.write(bytes(self.passive_command))
        await asyncio.sleep(0.5)
        self.uart.read(33)
        self.uart.write(bytes(self.read_command))
        await asyncio.sleep(0.5)
        response = self.uart.read(32)
        if not response:
            return None
        a = list(response)
        pm1 = a[10]*256+a[11]
        pm25 = a[12]*256+a[13]
        pm10 = a[14]*256+a[15]
        return {"pm1": pm1, "pm25": pm25, "pm10": pm10}
