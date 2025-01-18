from enum import Enum

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

from src.uart import Uart

BIT_0 = 0x0001
BIT_1 = 0x0002
BIT_2 = 0x0004
BIT_3 = 0x0008

BIT_4 = 0x0010
BIT_5 = 0x0020
BIT_6 = 0x0040
BIT_7 = 0x0080

BIT_8 = 0x0100
BIT_9 = 0x0200
BIT_10 = 0x0400
BIT_11 = 0x0800

BIT_12 = 0x1000
BIT_13 = 0x2000
BIT_14 = 0x4000
BIT_15 = 0x8000



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.uart = Uart()
        self.timer.timeout.connect(self.perform_action)
        self.timer.start(100)

        self.setWindowTitle("My App")
        self.setGeometry(100, 100, 800, 600)

        loadUi("./qt.ui", self)

        # self.background_task = BackgroundTask(buffer)
        # self.background_task.start()

    def perform_action(self):
        try:
            self.uart.write_data('012345678901')
            raw_buffer = self.uart.read_data()
            buffer = self.refine_buffer(raw_buffer)
            self.set_values_from_buffer(buffer)

        except Exception as e:
            print(f'error {e}')

    @staticmethod
    def refine_buffer(raw_buffer: bytes) -> dict[int, str]:
        buffer = [bin(word).removeprefix('0b') for word in raw_buffer]
        refined_buffer = dict()
        index = 0
        for word in buffer:
            refined_buffer[index] = word[index * 2] + word[index * 2 + 1]
            index += 1
        return refined_buffer

    def set_values_from_buffer(self, buffer: dict[int, str]) -> None:

        # addr=0x0021 0 5
        self.kanaly.setText(buffer[0] and 0x0fff)
        self.pr9A317M.setText(buffer[0] and BIT_15)

        # addr=0x0022 1 5
        self.sbrosy.setText(buffer[1] and 0x0fff)
        self.nal_R51.setText(buffer[1] and BIT_14)
        self.ots_R36.setText(buffer[1] and BIT_13)
        self.serv_po.setText(buffer[1] and BIT_12)

        # addr=0x0023 0 1 5
        self.sbros_strok.setText(buffer[2] and BIT_13)
        self.stroki.setText(buffer[2] and 0x1f00)
        self.otkaz_ot_CU.setText(buffer[2] and BIT_7)
        self.peresbros.setText(buffer[2] and BIT_6)
        self.inerc_sopr.setText(buffer[2] and BIT_5)
        self.pom_prin_c.setText(buffer[2] and BIT_4)
        self.zapros.setText(buffer[2] and BIT_3)
        self.sbr_zahv.setText(buffer[2] and BIT_2)
        self.razr_zahv.setText(buffer[2] and BIT_1)

        # addr=0x0024 2 5
        self.ubyv_lchm.setText(buffer[3] and BIT_11)
        self.p_avt_D.setText(buffer[3] and BIT_10)
        self.ruchn_Fd.setText(buffer[3] and BIT_9)
        self.avt_smena_izl.setText(buffer[3] and BIT_8)
        self.zahv_ruchn.setText(buffer[3] and BIT_7)
        self.dist_120.setText(buffer[3] and BIT_6)
        self.lchm_komb.setText(buffer[3] and BIT_5)
        self.dist_40.setText(buffer[3] and BIT_4)
        self.obrab_sdc.setText(buffer[3] and BIT_3)
        self.izl_lchm.setText(buffer[3] and BIT_2)
        self.izl_kni.setText(buffer[3] and BIT_1)
        self.avt_rab.setText(buffer[3] and BIT_0)

        # addr=0x0025 0 2 5
        self.att20.setText(buffer[4] and BIT_11)
        self.karta_mestn.setText(buffer[4] and BIT_10)
        self.avt_pomeh.setText(buffer[4] and BIT_9)
        self.obzor_nereg.setText(buffer[4] and BIT_7)
        self.razr_peresr.setText(buffer[4] and BIT_6)
        self.att60.setText(buffer[4] and BIT_2)
        self.att40.setText(buffer[4] and BIT_1)
        self.pom_prin_0.setText(buffer[4] and BIT_0)

        # addr=0x0026 1 2 5
        self.kontr_ib3_100.setText(buffer[5] and BIT_11)
        self.korr_ib3_100.setText(buffer[5] and BIT_10)
        self.perezap_ib3_100.setText(buffer[5] and BIT_9)
        self.podg_8.setText(buffer[5] and BIT_8)
        self.podg_3.setText(buffer[5] and BIT_7)
        self.extr_podgot.setText(buffer[5] and BIT_6)
        self.podgot.setText(buffer[5] and BIT_5)
        self.afk_mfrls.setText(buffer[5] and BIT_4)
        self.poisk_neipr.setText(buffer[5] and BIT_3)
        self.vkl_vys.setText(buffer[5] and BIT_2)
        self.vkl_ekv.setText(buffer[5] and BIT_1)
        self.liter_vv.setText(buffer[5] and BIT_0)

        # addr=0x0027 0 1 2 5
        self.tochka.setText(buffer[6] and BIT_10)
        self.tire.setText(buffer[6] and BIT_9)
        self.str_left.setText(buffer[6] and BIT_8)
        self.str_right.setText(buffer[6] and BIT_7)
        self.str_down.setText(buffer[6] and BIT_6)
        self.str_up.setText(buffer[6] and BIT_5)
        self.sloy_down.setText(buffer[6] and BIT_4)
        self.sloy_up.setText(buffer[6] and BIT_3)
        self.otmena.setText(buffer[6] and BIT_2)
        self.vvod_inf.setText(buffer[6] and BIT_1)
        self.sbros_inf.setText(buffer[6] and BIT_0)

        # addr=0x0028 3 5
        self.chislo.setText(buffer[7] and 0x03ff)

        # addr=0x0028 0 3 5
        self.prizn_rpn.setText(buffer[8] and BIT_6)
        self.prizn_sou.setText(buffer[8] and BIT_5)
        self.p_avt_tov.setText(buffer[8] and BIT_4)
        self.vkl_tov.setText(buffer[8] and BIT_3)
        self.vkl_tov_b_izl.setText(buffer[8] and BIT_2)
        self.korr_tochn_tov.setText(buffer[8] and BIT_1)

        # addr=0x41 - 0x45
        self.acps0.setText(buffer[9] and 0x03ff)
        self.acps1.setText(buffer[10] and 0x03ff)
        self.acps2.setText(buffer[11] and 0x03ff)
        self.acps3.setText(buffer[12] and 0x03ff)
        self.acps4.setText(buffer[13] and 0x03ff)
        self.acps5.setText(buffer[14] and 0x03ff)

        # addr=0x0c01 - 0x0c13
        self.op0.setText(buffer[15])
        self.op1.setText(buffer[16])
        self.op2.setText(buffer[17])
        self.op3.setText(buffer[18])
        self.op4.setText(buffer[19])
        self.op5.setText(buffer[20])
        self.op6.setText(buffer[21])
        self.op7.setText(buffer[22])
        self.op8.setText(buffer[23])
        self.op9.setText(buffer[24])
        self.op10.setText(buffer[25])
        self.op11.setText(buffer[26])
        self.op12.setText(buffer[27])
        self.op13.setText(buffer[28])
        self.op14.setText(buffer[29])
        self.op15.setText(buffer[30])
        self.op16.setText(buffer[31])
        self.op17.setText(buffer[32])
