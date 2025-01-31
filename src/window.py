import logging
from typing import Any

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

from constants import (BIT_1, BIT_2, BIT_3, BIT_11, BIT_13, BIT_15, BIT_14, BIT_12, BIT_6, BIT_7, BIT_9, BIT_10, BIT_0,
                       BIT_4, BIT_5, BIT_8)
from uart import Uart, UartReadError


class MainWindow(QMainWindow):
    kanaly: Any
    pr9A317M: Any
    sbrosy: Any
    nal_R51: Any
    ots_R36: Any
    serv_po: Any

    sbros_strok: Any
    stroki: Any
    otkaz_ot_CU: Any
    peresbros: Any
    inerc_sopr: Any
    pom_prin_c: Any
    zapros: Any
    sbr_zahv: Any
    razr_zahv: Any

    ubyv_lchm: Any
    p_avt_D: Any
    ruchn_Fd: Any
    avt_smena_izl: Any
    zahv_ruchn: Any
    dist_120: Any
    lchm_komb: Any
    dist_40: Any
    obrab_sdc: Any
    izl_lchm: Any
    izl_kni: Any
    avt_rab: Any

    att20: Any
    karta_mestn: Any
    avt_pomeh: Any
    obzor_nereg: Any
    razr_peresr: Any
    att60: Any
    att40: Any
    pom_prin_o: Any

    kontr_ib3_100: Any
    korr_ib3_100: Any
    perezap_ib3_100: Any
    podg_8: Any
    podg_3: Any
    extr_podgot: Any
    podgot: Any
    afk_mfrls: Any
    poisk_neispr: Any
    vkl_vys: Any
    vkl_ekv: Any
    liter_vv: Any

    tochka: Any
    tire: Any
    str_left: Any
    str_right: Any
    str_down: Any
    str_up: Any
    sloy_down: Any
    sloy_up: Any
    otmena: Any
    vvod_inf: Any
    sbros_inf: Any

    chislo: Any

    prizn_rpn: Any
    prizn_sou: Any
    p_avt_tov: Any
    vkl_tov: Any
    vkl_tov_b_izl: Any
    korr_tochn_tov: Any

    acps60: Any
    acps61: Any
    acps610: Any
    acps62: Any
    acps620: Any
    acps621: Any

    op0: Any
    op1: Any
    op2: Any
    op3: Any
    op4: Any
    op5: Any
    op6: Any
    op7: Any
    op8: Any
    op9: Any
    op10: Any
    op11: Any
    op12: Any
    op13: Any
    op14: Any
    op15: Any
    op16: Any
    op17: Any

    radio_lchm: Any
    radio_40: Any
    checkBox_kontrol: Any
    checkBox_zapros: Any
    checkBox_sopr: Any
    checkBox_strobir: Any
    checkBox_obzor: Any

    oo_delay: Any
    leds1: Any
    leds2: Any
    leds3: Any
    leds4: Any
    leds5: Any

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
            if self.uart.exchange_count > 9:
                self.uart.exchange_count = 0
            else:
                self.uart.exchange_count += 1
            self.com_exchange.setText(f'{self.uart.exchange_count}')

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
        self.kanaly.setText(f'Каналы\t{bin(temp & 0x0fff)[2:]:012}')
        self.pr9A317M.setText(f'Призн 9А317М\t{bin(temp & BIT_15)[2:]}')

        # addr=0x0022 1 5
        temp = buffer[3]
        self.sbrosy.setText(f'Сбросы\t{bin(temp & 0x0fff)[2:]:012}')
        self.nal_R51.setText(f'Наличие Р51\t{bin(temp & BIT_14)[2:]}')
        self.ots_R36.setText(f'Отс Р36\t{bin(temp & BIT_13)[2:]}')
        self.serv_po.setText(f'Серв. ПО\t{bin(temp & BIT_12)[2:]}')

        # addr=0x0023 0 1 5
        temp = buffer[4]
        self.sbros_strok.setText(f'Сброс строк\t{bin(temp & BIT_13)[2:]}')
        self.stroki.setText(f'Строки\t\t{bin(temp & 0x1f00)[2:]:05}')
        self.otkaz_ot_CU.setText(f'Отказ от ЦУ\t{bin(temp & BIT_7)[2:]}')
        self.peresbros.setText(f'Переброс\t{bin(temp & BIT_6)[2:]}')
        self.inerc_sopr.setText(f'Инерц сопр\t{bin(temp & BIT_5)[2:]}')
        self.pom_prin_c.setText(f'Пом прин С\t{bin(temp & BIT_4)[2:]}')
        self.zapros.setText(f'Запрос\t\t{bin(temp & BIT_3)[2:]}')
        self.sbr_zahv.setText(f'Сбр захв\t{bin(temp & BIT_2)[2:]}')
        self.razr_zahv.setText(f'Разр захв\t{bin(temp & BIT_1)[2:]}')

        # addr=0x0024 2 5
        temp = buffer[5]
        self.ubyv_lchm.setText(f'Убыв ЛЧМ\t{bin(temp & BIT_11)[2:]}')
        self.p_avt_D.setText(f'П/АВТ Д\t{bin(temp & BIT_10)[2:]}')
        self.ruchn_Fd.setText(f'Ручн Fд\t{bin(temp & BIT_9)[2:]}')
        self.avt_smena_izl.setText(f'Авт смена изл\t{bin(temp & BIT_8)[2:]}')
        self.zahv_ruchn.setText(f'Захв ручн\t{bin(temp & BIT_7)[2:]}')
        self.dist_120.setText(f'Дист 120\t{bin(temp & BIT_6)[2:]}')
        self.lchm_komb.setText(f'ЛЧМ комб\t{bin(temp & BIT_5)[2:]}')
        self.dist_40.setText(f'Дист 40\t{bin(temp & BIT_4)[2:]}')
        self.obrab_sdc.setText(f'Обраб СДЦ\t{bin(temp & BIT_3)[2:]}')
        self.izl_lchm.setText(f'Изл ЛЧМ\t{bin(temp & BIT_2)[2:]}')
        self.izl_kni.setText(f'Изл КНИ\t{bin(temp & BIT_1)[2:]}')
        self.avt_rab.setText(f'Авт раб\t{bin(temp & BIT_0)[2:]}')

        # addr=0x0025 0 2 5
        temp = buffer[6]
        self.att20.setText(f'Затух 20\t{bin(temp & BIT_11)[2:]}')
        self.karta_mestn.setText(f'Карта местн\t{bin(temp & BIT_10)[2:]}')
        self.avt_pomeh.setText(f'Авт пом\t{bin(temp & BIT_9)[2:]}')
        self.obzor_nereg.setText(f'Обзор нерег\t{bin(temp & BIT_7)[2:]}')
        self.razr_peresr.setText(f'Разр перест\t{bin(temp & BIT_6)[2:]}')
        self.att60.setText(f'Затух 60\t{bin(temp & BIT_2)[2:]}')
        self.att40.setText(f'Затух 40\t{bin(temp & BIT_1)[2:]}')
        self.pom_prin_o.setText(f'Пом прин О\t{bin(temp & BIT_0)[2:]}')

        # addr=0x0026 1 2 5
        temp = buffer[7]
        self.kontr_ib3_100.setText(f'Контр ИБ3 100\t\t{bin(temp & BIT_11)[2:]}')
        self.korr_ib3_100.setText(f'Корр ИБ3 100\t\t{bin(temp & BIT_10)[2:]}')
        self.perezap_ib3_100.setText(f'Перезап ИБ3 100\t{bin(temp & BIT_9)[2:]}')
        self.podg_8.setText(f'Подг 8\t\t\t{bin(temp & BIT_8)[2:]}')
        self.podg_3.setText(f'Подг 3\t\t\t{bin(temp & BIT_7)[2:]}')
        self.extr_podgot.setText(f'Эктр. подгот\t\t{bin(temp & BIT_6)[2:]}')
        self.podgot.setText(f'Подгот\t\t\t{bin(temp & BIT_5)[2:]}')
        self.afk_mfrls.setText(f'АФК МФРЛС\t\t{bin(temp & BIT_4)[2:]}')
        self.poisk_neispr.setText(f'Поиск неиспр\t\t{bin(temp & BIT_3)[2:]}')
        self.vkl_vys.setText(f'Вкл выс\t\t{bin(temp & BIT_2)[2:]}')
        self.vkl_ekv.setText(f'Вкл экв\t\t\t{bin(temp & BIT_1)[2:]}')
        self.liter_vv.setText(f'Литер ВВ\t\t{bin(temp & BIT_0)[2:]}')

        # addr=0x0027 0 1 2 5
        temp = buffer[8]
        self.tochka.setText(f'Точка\t\t{bin(temp & BIT_10)[2:]}')
        self.tire.setText(f'Тире\t\t{bin(temp & BIT_9)[2:]}')
        self.str_left.setText(f'Стр лево\t{bin(temp & BIT_8)[2:]}')
        self.str_right.setText(f'Стр право\t{bin(temp & BIT_7)[2:]}')
        self.str_down.setText(f'Стр вниз\t{bin(temp & BIT_6)[2:]}')
        self.str_up.setText(f'Стр вверх\t{bin(temp & BIT_5)[2:]}')
        self.sloy_down.setText(f'Слой вниз\t{bin(temp & BIT_4)[2:]}')
        self.sloy_up.setText(f'Слой вверх\t{bin(temp & BIT_3)[2:]}')
        self.otmena.setText(f'Отмена\t{bin(temp & BIT_2)[2:]}')
        self.vvod_inf.setText(f'Ввод инф\t{bin(temp & BIT_1)[2:]}')
        self.sbros_inf.setText(f'Сброс инф\t{bin(temp & BIT_0)[2:]}')

        # addr=0x0028 3 5
        temp = buffer[9]
        self.chislo.setText(f'Число\t{bin(temp & 0x03ff)[2:]:010}')

        # addr=0x0028 0 3 5
        temp = buffer[10]
        self.prizn_rpn.setText(f'Призн РПН\t\t{bin(temp & BIT_6)[2:]}')
        self.prizn_sou.setText(f'Призн СОУ\t\t{bin(temp & BIT_5)[2:]}')
        self.p_avt_tov.setText(f'П/авт ТОВ\t\t{bin(temp & BIT_4)[2:]}')
        self.vkl_tov.setText(f'Вкл ТОВ\t\t{bin(temp & BIT_3)[2:]}')
        self.vkl_tov_b_izl.setText(f'Вкл ТОВ без изл\t{bin(temp & BIT_2)[2:]}')
        self.korr_tochn_tov.setText(f'Корр точн ТОВ\t{bin(temp & BIT_1)[2:]}')

        # addr=0x41 - 0x45
        self.acps60.setText(f'АЦПС 6 0 \t{str((buffer[11] & 0x03ff) - 512)}')
        self.acps61.setText(f'АЦПС 6 1 \t{str((buffer[12] & 0x03ff) - 512)}')
        self.acps610.setText(f'АЦПС 6 1 0 \t{str((buffer[13] & 0x03ff) - 512)}')
        self.acps62.setText(f'АЦПС 6 2 \t{str((buffer[14] & 0x03ff) - 512)}')
        self.acps620.setText(f'АЦПС 6 2 0 \t{str((buffer[15] & 0x03ff) - 512)}')
        self.acps621.setText(f'АЦПС 6 2 1 \t{str((buffer[16] & 0x03ff) - 512)}')

        # addr=0x0c01 - 0x0c13
        self.op0.setText(f'{bin(buffer[17])[2:]:016}')
        self.op1.setText(f'{bin(buffer[18])[2:]:016}')
        self.op2.setText(f'{bin(buffer[19])[2:]:016}')
        self.op3.setText(f'{bin(buffer[20])[2:]:016}')
        self.op4.setText(f'{bin(buffer[21])[2:]:016}')
        self.op5.setText(f'{bin(buffer[22])[2:]:016}')
        self.op6.setText(f'{bin(buffer[23])[2:]:016}')
        self.op7.setText(f'{bin(buffer[24])[2:]:016}')
        self.op8.setText(f'{bin(buffer[25])[2:]:016}')
        self.op9.setText(f'{bin(buffer[26])[2:]:016}')
        self.op10.setText(f'{bin(buffer[27])[2:]:016}')
        self.op11.setText(f'{bin(buffer[28])[2:]:016}')
        self.op12.setText(f'{bin(buffer[29])[2:]:016}')
        self.op13.setText(f'{bin(buffer[30])[2:]:016}')
        self.op14.setText(f'{bin(buffer[31])[2:]:016}')
        self.op15.setText(f'{bin(buffer[32])[2:]:016}')
        self.op16.setText(f'{bin(buffer[33])[2:]:016}')
        self.op17.setText(f'{bin(buffer[34])[2:]:016}')

    @staticmethod
    def convert(data: int) -> tuple[int, int]:
        return data & 0xff, data >> 8
