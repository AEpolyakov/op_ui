import serial.tools.list_ports
import logging

UART_SPEED = 9600

def init_uart():
    ports = list(serial.tools.list_ports.comports())

    port = None
    for port in ports:
        if port.manufacturer == 'wch.cn':
            port = port.device
            break

    if port is None:
        error_msg = 'No serial port found'
        logging.error(error_msg)
        raise Exception(error_msg)

    logging.info(f'USB-uart finded on {port}')

    uart = serial.Serial(port, UART_SPEED)

    logging.info(f'USB-uart {port} connected')

    return uart