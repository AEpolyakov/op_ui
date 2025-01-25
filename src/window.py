import logging
import time

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

from constants import (BIT_1, BIT_2, BIT_3, BIT_11, BIT_13)
from uart import Uart, UartReadError


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        try:
            self.uart = Uart()
        except Exception as e:
            logging.error(e)

        self.timer.timeout.connect(self.exchange)
        self.timer.start(100)

        self.setWindowTitle("My App")
        self.setGeometry(100, 100, 800, 600)

        loadUi("./qt.ui", self)

    def exchange(self):
        try:
            data_to_send = self.get_values_from_prog()
            self.uart.write_data(data_to_send)

            raw_buffer = self.uart.read_data()

            self.com_status.setText(f'{self.uart.port} Подключен')

            buffer = self.refine_buffer(raw_buffer)
            self.set_values_from_buffer(buffer)

        except UartReadError as e:
            self.com_status.setText(f'{self.uart.port} Ошибка')
            logging.error('Ошибка чтения UART')
        except Exception as e:
            logging.error(f'Ошибка {e}')

    def get_values_from_prog(self) -> bytes:
        buff = []

        # kni = self.radio_kni.isChecked()
        lchm = self.radio_lchm.isChecked()
        dist40 = self.radio_40.isChecked()
        # dist120 = self.radio_120.isChecked()
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
        refined_buffer = dict()

        for index in range(self.uart.buffer_len // 2):
            refined_buffer[index] = int(raw_buffer[index * 2 + 1] + raw_buffer[index * 2], 16)

        return refined_buffer

    def set_values_from_buffer(self, buffer: dict[int, int]) -> None:

        # addr=0x0021 0 5
        temp = buffer[2]
        self.kanaly.setText(bin(temp & 0x0fff)[2:])
        # self.pr9A317M.setText(bin(temp & BIT_15)[2:])

        # addr=0x0022 1 5
        temp = buffer[3]
        self.sbrosy.setText(bin(temp & 0x0fff)[2:])
        # self.nal_R51.setText(bin(temp & BIT_14 )[2:])
        # self.ots_R36.setText(bin(temp & BIT_13 )[2:])
        # self.serv_po.setText(bin(temp & BIT_12 )[2:])

        # addr=0x0023 0 1 5
        temp = buffer[4]
        self.sbros_strok.setText(bin(temp & BIT_13)[2:])
        self.stroki.setText(bin(temp & 0x1f00)[2:])
        # self.otkaz_ot_CU.setText(bin(temp & BIT_7 )[2:])
        # self.peresbros.setText(bin(temp & BIT_6 )[2:])
        # self.inerc_sopr.setText(bin(temp & BIT_5 )[2:])
        # self.pom_prin_c.setText(bin(temp & BIT_4 )[2:])
        self.zapros.setText(bin(temp & BIT_3)[2:])
        self.sbr_zahv.setText(bin(temp & BIT_2)[2:])
        self.razr_zahv.setText(bin(temp & BIT_1)[2:])

        # addr=0x0024 2 5
        temp = buffer[5]
        # self.ubyv_lchm.setText(bin(temp & BIT_11)[2:])
        # self.p_avt_D.setText(bin(temp & BIT_10)[2:])
        # self.ruchn_Fd.setText(bin(temp & BIT_9)[2:])
        # self.avt_smena_izl.setText(bin(temp & BIT_8)[2:])
        # self.zahv_ruchn.setText(bin(temp & BIT_7)[2:])
        # self.dist_120.setText(bin(temp & BIT_6)[2:])
        # self.lchm_komb.setText(bin(temp & BIT_5)[2:])
        # self.dist_40.setText(bin(temp & BIT_4)[2:])
        # self.obrab_sdc.setText(bin(temp & BIT_3)[2:])
        # self.izl_lchm.setText(bin(temp & BIT_2)[2:])
        # self.izl_kni.setText(bin(temp & BIT_1)[2:])
        # self.avt_rab.setText(bin(temp & BIT_0)[2:])

        # addr=0x0025 0 2 5
        temp = buffer[6]
        self.att20.setText(bin(temp & BIT_11)[2:])
        # self.karta_mestn.setText(bin(temp & BIT_10)[2:])
        # self.avt_pomeh.setText(bin(temp & BIT_9)[2:])
        # self.obzor_nereg.setText(bin(temp & BIT_7)[2:])
        # self.razr_peresr.setText(bin(temp & BIT_6)[2:])
        self.att60.setText(bin(temp & BIT_2)[2:])
        self.att40.setText(bin(temp & BIT_1)[2:])
        # self.pom_prin_0.setText(bin(temp & BIT_0)[2:])

        # addr=0x0026 1 2 5
        temp = buffer[7]
        # self.kontr_ib3_100.setText(bin(temp & BIT_11)[2:])
        # self.korr_ib3_100.setText(bin(temp & BIT_10)[2:])
        # self.perezap_ib3_100.setText(bin(temp & BIT_9)[2:])
        # self.podg_8.setText(bin(temp & BIT_8)[2:])
        # self.podg_3.setText(bin(temp & BIT_7)[2:])
        # self.extr_podgot.setText(bin(temp & BIT_6)[2:])
        # self.podgot.setText(bin(temp & BIT_5)[2:])
        # self.afk_mfrls.setText(bin(temp & BIT_4)[2:])
        # self.poisk_neipr.setText(bin(temp & BIT_3)[2:])
        # self.vkl_vys.setText(bin(temp & BIT_2)[2:])
        # self.vkl_ekv.setText(bin(temp & BIT_1)[2:])
        # self.liter_vv.setText(bin(temp & BIT_0)[2:])

        # addr=0x0027 0 1 2 5
        temp = buffer[8]
        # self.tochka.setText(bin(temp & BIT_10)[2:])
        # self.tire.setText(bin(temp & BIT_9)[2:])
        # self.str_left.setText(bin(temp & BIT_8)[2:])
        # self.str_right.setText(bin(temp & BIT_7)[2:])
        # self.str_down.setText(bin(temp & BIT_6)[2:])
        # self.str_up.setText(bin(temp & BIT_5)[2:])
        # self.sloy_down.setText(bin(temp & BIT_4)[2:])
        # self.sloy_up.setText(bin(temp & BIT_3)[2:])
        # self.otmena.setText(bin(temp & BIT_2)[2:])
        # self.vvod_inf.setText(bin(temp & BIT_1)[2:])
        # self.sbros_inf.setText(bin(temp & BIT_0)[2:])

        # addr=0x0028 3 5
        temp = buffer[9]
        # self.chislo.setText(bin(temp & 0x03ff)[2:])

        # addr=0x0028 0 3 5
        temp = buffer[10]
        # self.prizn_rpn.setText(bin(temp & BIT_6)[2:])
        # self.prizn_sou.setText(bin(temp & BIT_5)[2:])
        # self.p_avt_tov.setText(bin(temp & BIT_4)[2:])
        # self.vkl_tov.setText(bin(temp & BIT_3)[2:])
        # self.vkl_tov_b_izl.setText(bin(temp & BIT_2)[2:])
        # self.korr_tochn_tov.setText(bin(temp & BIT_1)[2:])

        # addr=0x41 - 0x45
        self.acps60.setText(str((buffer[11] & 0x03ff) - 512))
        self.acps61.setText(str((buffer[12] & 0x03ff) - 512))
        self.acps610.setText(str((buffer[13] & 0x03ff) - 512))
        self.acps62.setText(str((buffer[14] & 0x03ff) - 512))
        self.acps620.setText(str((buffer[15] & 0x03ff) - 512))
        self.acps621.setText(str((buffer[16] & 0x03ff) - 512))

        # addr=0x0c01 - 0x0c13
        self.op0.setText(bin(buffer[17])[2:])
        self.op1.setText(bin(buffer[18])[2:])
        self.op2.setText(bin(buffer[19])[2:])
        self.op3.setText(bin(buffer[20])[2:])
        self.op4.setText(bin(buffer[21])[2:])
        self.op5.setText(bin(buffer[22])[2:])
        self.op6.setText(bin(buffer[23])[2:])
        self.op7.setText(bin(buffer[24])[2:])
        self.op8.setText(bin(buffer[25])[2:])
        self.op9.setText(bin(buffer[26])[2:])
        self.op10.setText(bin(buffer[27])[2:])
        self.op11.setText(bin(buffer[28])[2:])
        self.op12.setText(bin(buffer[29])[2:])
        self.op13.setText(bin(buffer[30])[2:])
        self.op14.setText(bin(buffer[31])[2:])
        self.op15.setText(bin(buffer[32])[2:])
        self.op16.setText(bin(buffer[33])[2:])
        self.op17.setText(bin(buffer[34])[2:])

    @staticmethod
    def convert(data: int) -> tuple[int, int]:
        return data & 0xff, data >> 8
