import logging

import serial.tools.list_ports

UART_SPEED = 115200


class UartReadError(Exception):
    ...


class Uart:
    buffer_len = 74

    def __init__(self, speed=UART_SPEED):
        self.data = []
        self.connection = None
        self.port = None
        self.data = None
        self.speed = speed
        self.init_uart()
        self.exchange_count = 0

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
        self.connection = serial.Serial(self.port, self.speed, timeout=0.1)
        logging.info(f'USB-uart {self.port} connected')

    def write_data(self, data: bytes):
        self.connection.write(data)
        logging.info(f'USB write {data}')

    def read_data(self) -> dict[int, str]:
        data = dict()
        for i in range(self.buffer_len):
            data[i] = self.connection.read().hex()

        if not (
                data[1] == 'de' and
                data[0] == 'ad' and
                data[3] == 'be' and
                data[2] == 'ef' and
                data[self.buffer_len - 3] == 'de' and
                data[self.buffer_len - 4] == 'ad' and
                data[self.buffer_len - 1] == 'be' and
                data[self.buffer_len - 2] == 'ef'
        ):
            raise UartReadError('end byte error')

        return data
