import logging
from dataclasses import dataclass

import serial.tools.list_ports

mock_data = ['0000', '0000', '0000', '0001', '0000', '0000', '0000', '0000', '0000', '0000',
             '0000', '0000', '0000', '0000', '0000', '0000', '0000', '0000']
UART_SPEED = 115200

@dataclass
class Bitmap:
    mark = (0, 155, 0)
    background = (200, 200, 200)


class Uart:

    def __init__(self, speed=UART_SPEED):
        self.data = []
        self.connection = None
        self.port = None
        self.data = None
        self.speed = speed
        self.init_uart()

    def init_uart(self):
        ports = list(serial.tools.list_ports.comports())

        for port in ports:
            if port.manufacturer == 'wch.cn':
                self.port = port.device
                break

        if self.port is None:
            error_msg = 'No serial port found'
            logging.error(error_msg)
            raise Exception(error_msg)

        logging.info(f'Find USB-uart on {self.port}')
        self.connection = serial.Serial(self.port, self.speed)
        logging.info(f'USB-uart {self.port} connected')

    def send_data(self, sent_data: list[str]) -> list[str]:
        self.data = mock_data
        logging.info(f'Exchange. Sent: {len(sent_data)}. Received: {len(self.data)}')
        return self.data

    def read_data(self):
        return self.connection.readline().decode().strip()

    # def get_op_image(self):
    #
    #     screen_width = 200
    #     op_distance = []
    #     op_bitmap = []
    #     for word in self.data:
    #         for i in range(4):
    #             char: int = int(word[i], 16)
    #             t = []
    #             for j in range(4):
    #                 bit = Bitmap.mark if char & 1 else Bitmap.background
    #                 t.append(bit)
    #                 char = char >> 1
    #             t.reverse()
    #             op_distance.extend(t)
    #     for i in range(screen_width):
    #         op_bitmap.extend(op_distance)
    #     array = np.array(op_bitmap)
    #
    #     array = np.reshape(array, (screen_width, 288, 3))
    #
    #     array = np.transpose(array, (1, 0, 2))
    #     array = np.flip(array, 0)
    #
    #     return im.fromarray(array.astype(np.uint8))
