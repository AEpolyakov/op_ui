import logging

import serial.tools.list_ports

UART_SPEED = 115200


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

    def write_data(self, data: str):
        data_bytes = data.encode('utf-8')
        self.connection.write(data_bytes)
        logging.info(f'USB write {data}')

    def read_data(self) -> bytes:
        data = self.connection.readline(66)
        logging.info(f'USB read {data}; length={len(data)}')
        return data

