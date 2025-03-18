import logging

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

from src.main_window_def import MainWindowDef
from uart import Uart, UartReadError


class MainWindow(QMainWindow, MainWindowDef):

    def update_image(self, op_data: list[int]):
        width, height = 50, 288

        image = QImage(width, height, QImage.Format.Format_RGB888)
        image.fill(Qt.GlobalColor.black)

        for y in range(height):
            if op_data[y] == 1:
                for x in range(width):
                    image.setPixelColor(x, y, Qt.GlobalColor.green)

        image = image.mirrored(vertical=True)
        pixmap = QPixmap.fromImage(image)

        self.op_image.setPixmap(pixmap)

    def __init__(self):
        super().__init__()

        loadUi("./qt.ui", self)

        self.setWindowIcon(QIcon("cosd.ico"))

        self.timer = QTimer()

        try:
            self.uart = Uart()
        except Exception as e:
            logging.error(e)

        self.timer.timeout.connect(self.exchange)
        self.timer.start(100)

    def exchange(self):
        raw_buffer = []
        data_to_send = self.get_values_from_interface()
        self.uart.write_data(data_to_send)

        try:
            raw_buffer = self.uart.read_data()
        except UartReadError as e:
            self.com_status.setText(f'{self.uart.port} Ошибка')
            logging.error(f'Ошибка чтения UART {e}')
        except Exception as e:
            logging.error(f'Ошибка {e}')

        self.com_status.setText(f'{self.uart.port} Подключен')
        if self.uart.exchange_count > 9:
            self.uart.exchange_count = 0
        else:
            self.uart.exchange_count += 1
        self.com_exchange.setText(f'{self.uart.exchange_count}')

        buffer = self.refine_buffer(raw_buffer)
        self.set_values_from_buffer(buffer)

        self.update_image(self.refine_op_data(buffer))

    @staticmethod
    def refine_op_data(buffer: dict[int, int]) -> list[int]:
        """Преобразовать буфер полученный из оп размера 18x16 в одномерный массив размера 288x1"""
        op_words = []
        for index, value in buffer.items():
            if 17 <= index <= 34:
                op_words.append(value)
        op_data = []
        for word in op_words:
            temp = word
            for bit in range(16):
                op_data.append(temp & 1)
                temp = temp >> 1
        return op_data

    def get_values_from_interface(self) -> bytes:
        """Получить значения заданные в интерфейсе программы."""
        buff = []

        lchm = self.radio_lchm.isChecked()
        dist40 = self.radio_40.isChecked()
        kontrol = self.checkBox_kontrol.isChecked()
        zapros = self.checkBox_zapros.isChecked()
        sopr = self.checkBox_sopr.isChecked()
        strobir = self.checkBox_strobir.isChecked()
        obzor = self.checkBox_obzor.isChecked()

        op_command_l = kontrol * 128 + sopr * 64 + obzor * 32 + strobir * 16 + lchm * 8 + zapros * 2
        op_command_h = dist40 * 1

        oo_delay = int(self.oo_delay.text())
        leds1 = int(self.leds1.text(), 16)
        leds2 = int(self.leds2.text(), 16)
        leds3 = int(self.leds3.text(), 16)
        leds4 = int(self.leds4.text(), 16)
        leds5 = int(self.leds5.text(), 16)

        buff.append(op_command_l)
        buff.append(op_command_h)
        buff.extend(self.convert(oo_delay))
        buff.extend(self.convert(leds1))
        buff.extend(self.convert(leds2))
        buff.extend(self.convert(leds3))
        buff.extend(self.convert(leds4))
        buff.extend(self.convert(leds5))

        return b''.join((el.to_bytes() for el in buff))

    def refine_buffer(self, raw_buffer: dict[int, str]) -> dict[int, int]:
        """Преобразование списка 74x8 бит в словарь 36x16"""
        refined_buffer = dict()

        for index in range(self.uart.buffer_len // 2):
            refined_buffer[index] = int(raw_buffer[index * 2 + 1] + raw_buffer[index * 2], 16)

        return refined_buffer

    @staticmethod
    def get_bit_value(temp: int, bit: int) -> str:
        return bin((temp >> bit) & 1)[2:]

    @staticmethod
    def get_bits_value(temp: int, start_bit: int, n_bits: int) -> str:
        mask = pow(2, n_bits) - 1
        return f'{bin((temp >> start_bit) & mask)[2:]:0>{n_bits}}'

    def set_values_from_buffer(self, buffer: dict[int, int]) -> None:

        # addr=0x0021 0 5
        temp = buffer[2]
        self.kanaly.setText(f'Каналы\t\t{self.get_bits_value(temp, 0, 12)}')
        self.pr9A317M.setText(f'Призн 9А317М\t{self.get_bit_value(temp, 15)}')

        # addr=0x0022 1 5
        temp = buffer[3]
        self.sbrosy.setText(f'Сбросы\t\t{self.get_bits_value(temp, 0, 12)}')
        self.nal_R51.setText(f'Наличие Р51\t{self.get_bit_value(temp, 14)}')
        self.ots_R36.setText(f'Отс Р36\t\t{self.get_bit_value(temp, 13)}')
        self.serv_po.setText(f'Серв. ПО\t{self.get_bit_value(temp, 12)}')

        # addr=0x0023 0 1 5
        temp = buffer[4]
        self.sbros_strok.setText(f'Сброс строк\t{self.get_bit_value(temp, 13)}')
        self.stroki.setText(f'Строки\t\t{self.get_bits_value(temp, 8, 5)}')
        self.otkaz_ot_CU.setText(f'Отказ от ЦУ\t{self.get_bit_value(temp, 7)}')
        self.peresbros.setText(f'Переброс\t{self.get_bit_value(temp, 6)}')
        self.inerc_sopr.setText(f'Инерц сопр\t{self.get_bit_value(temp, 5)}')
        self.pom_prin_c.setText(f'Пом прин С\t{self.get_bit_value(temp, 4)}')
        self.zapros.setText(f'Запрос\t\t{self.get_bit_value(temp, 3)}')
        self.sbr_zahv.setText(f'Сбр захв\t{self.get_bit_value(temp, 2)}')
        self.razr_zahv.setText(f'Разр захв\t{self.get_bit_value(temp, 1)}')

        # addr=0x0024 2 5
        temp = buffer[5]
        self.ubyv_lchm.setText(f'Убыв ЛЧМ\t{self.get_bit_value(temp, 11)}')
        self.p_avt_D.setText(f'П/АВТ Д\t\t{self.get_bit_value(temp, 10)}')
        self.ruchn_Fd.setText(f'Ручн Fд\t\t{self.get_bit_value(temp, 9)}')
        self.avt_smena_izl.setText(f'Авт смена изл\t{self.get_bit_value(temp, 8)}')
        self.zahv_ruchn.setText(f'Захв ручн\t{self.get_bit_value(temp, 7)}')
        self.dist_120.setText(f'Дист 120\t{self.get_bit_value(temp, 6)}')
        self.lchm_komb.setText(f'ЛЧМ комб\t{self.get_bit_value(temp, 5)}')
        self.dist_40.setText(f'Дист 40\t\t{self.get_bit_value(temp, 4)}')
        self.obrab_sdc.setText(f'Обраб СДЦ\t{self.get_bit_value(temp, 3)}')
        self.izl_lchm.setText(f'Изл ЛЧМ\t\t{self.get_bit_value(temp, 2)}')
        self.izl_kni.setText(f'Изл КНИ\t\t{self.get_bit_value(temp, 1)}')
        self.avt_rab.setText(f'Авт раб\t\t{self.get_bit_value(temp, 0)}')

        # addr=0x0025 0 2 5
        temp = buffer[6]
        self.att20.setText(f'Затух 20\t{self.get_bit_value(temp, 11)}')
        self.karta_mestn.setText(f'Карта местн\t{self.get_bit_value(temp, 10)}')
        self.avt_pomeh.setText(f'Авт пом\t\t{self.get_bit_value(temp, 9)}')
        self.obzor_nereg.setText(f'Обзор нерег\t{self.get_bit_value(temp, 7)}')
        self.razr_peresr.setText(f'Разр перест\t{self.get_bit_value(temp, 6)}')
        self.att60.setText(f'Затух 60\t{self.get_bit_value(temp, 2)}')
        self.att40.setText(f'Затух 40\t{self.get_bit_value(temp, 1)}')
        self.pom_prin_o.setText(f'Пом прин О\t{self.get_bit_value(temp, 0)}')

        # addr=0x0026 1 2 5
        temp = buffer[7]
        self.kontr_ib3_100.setText(f'Контр ИБ3 100\t\t{self.get_bit_value(temp, 11)}')
        self.korr_ib3_100.setText(f'Корр ИБ3 100\t\t{self.get_bit_value(temp, 10)}')
        self.perezap_ib3_100.setText(f'Перезап ИБ3 100\t{self.get_bit_value(temp, 9)}')
        self.podg_8.setText(f'Подг 8\t\t\t{self.get_bit_value(temp, 8)}')
        self.podg_3.setText(f'Подг 3\t\t\t{self.get_bit_value(temp, 7)}')
        self.extr_podgot.setText(f'Эктр. подгот\t\t{self.get_bit_value(temp, 6)}')
        self.podgot.setText(f'Подгот\t\t\t{self.get_bit_value(temp, 5)}')
        self.afk_mfrls.setText(f'АФК МФРЛС\t\t{self.get_bit_value(temp, 4)}')
        self.poisk_neispr.setText(f'Поиск неиспр\t\t{self.get_bit_value(temp, 3)}')
        self.vkl_vys.setText(f'Вкл выс\t\t{self.get_bit_value(temp, 2)}')
        self.vkl_ekv.setText(f'Вкл экв\t\t\t{self.get_bit_value(temp, 1)}')
        self.liter_vv.setText(f'Литер ВВ\t\t{self.get_bit_value(temp, 0)}')

        # addr=0x0027 0 1 2 5
        temp = buffer[8]
        self.tochka.setText(f'Точка\t\t{self.get_bit_value(temp, 10)}')
        self.tire.setText(f'Тире\t\t{self.get_bit_value(temp, 9)}')
        self.str_left.setText(f'Стр лево\t{self.get_bit_value(temp, 8)}')
        self.str_right.setText(f'Стр право\t{self.get_bit_value(temp, 7)}')
        self.str_down.setText(f'Стр вниз\t{self.get_bit_value(temp, 6)}')
        self.str_up.setText(f'Стр вверх\t{self.get_bit_value(temp, 5)}')
        self.sloy_down.setText(f'Слой вниз\t{self.get_bit_value(temp, 4)}')
        self.sloy_up.setText(f'Слой вверх\t{self.get_bit_value(temp, 3)}')
        self.otmena.setText(f'Отмена\t{self.get_bit_value(temp, 2)}')
        self.vvod_inf.setText(f'Ввод инф\t{self.get_bit_value(temp, 1)}')
        self.sbros_inf.setText(f'Сброс инф\t{self.get_bit_value(temp, 0)}')

        # addr=0x0028 3 5
        temp = buffer[9]
        self.chislo.setText(f'Число\t{self.get_bits_value(temp, 0, 10)}')

        # addr=0x0028 0 3 5
        temp = buffer[10]
        self.prizn_rpn.setText(f'Призн РПН\t\t{self.get_bit_value(temp, 6)}')
        self.prizn_sou.setText(f'Призн СОУ\t\t{self.get_bit_value(temp, 5)}')
        self.p_avt_tov.setText(f'П/авт ТОВ\t\t{self.get_bit_value(temp, 4)}')
        self.vkl_tov.setText(f'Вкл ТОВ\t\t{self.get_bit_value(temp, 3)}')
        self.vkl_tov_b_izl.setText(f'Вкл ТОВ без изл\t{self.get_bit_value(temp, 2)}')
        self.korr_tochn_tov.setText(f'Корр точн ТОВ\t{self.get_bit_value(temp, 1)}')

        # addr=0x41 - 0x45
        self.acps60.setText(f'АЦПС 6 0 \t{str((buffer[11] & 0x03ff) - 512)}')
        self.acps61.setText(f'АЦПС 6 1 \t{str((buffer[12] & 0x03ff) - 512)}')
        self.acps610.setText(f'АЦПС 6 1 0 \t{str((buffer[13] & 0x03ff) - 512)}')
        self.acps62.setText(f'АЦПС 6 2 \t{str((buffer[14] & 0x03ff) - 512)}')
        self.acps620.setText(f'АЦПС 6 2 0 \t{str((buffer[15] & 0x03ff) - 512)}')
        self.acps621.setText(f'АЦПС 6 2 1 \t{str((buffer[16] & 0x03ff) - 512)}')

        # addr=0x0c01 - 0x0c13
        self.op0.setText(f'{bin(buffer[17])[2:]:0>16}')
        self.op1.setText(f'{bin(buffer[18])[2:]:0>16}')
        self.op2.setText(f'{bin(buffer[19])[2:]:0>16}')
        self.op3.setText(f'{bin(buffer[20])[2:]:0>16}')
        self.op4.setText(f'{bin(buffer[21])[2:]:0>16}')
        self.op5.setText(f'{bin(buffer[22])[2:]:0>16}')
        self.op6.setText(f'{bin(buffer[23])[2:]:0>16}')
        self.op7.setText(f'{bin(buffer[24])[2:]:0>16}')
        self.op8.setText(f'{bin(buffer[25])[2:]:0>16}')
        self.op9.setText(f'{bin(buffer[26])[2:]:0>16}')
        self.op10.setText(f'{bin(buffer[27])[2:]:0>16}')
        self.op11.setText(f'{bin(buffer[28])[2:]:0>16}')
        self.op12.setText(f'{bin(buffer[29])[2:]:0>16}')
        self.op13.setText(f'{bin(buffer[30])[2:]:0>16}')
        self.op14.setText(f'{bin(buffer[31])[2:]:0>16}')
        self.op15.setText(f'{bin(buffer[32])[2:]:0>16}')
        self.op16.setText(f'{bin(buffer[33])[2:]:0>16}')
        self.op17.setText(f'{bin(buffer[34])[2:]:0>16}')

    @staticmethod
    def convert(data: int) -> tuple[int, int]:
        return data & 0xff, data >> 8
