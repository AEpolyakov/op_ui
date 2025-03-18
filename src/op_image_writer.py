from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel


class OpImageWriter:

    @staticmethod
    def rewrite_image(op_data: list[int], op_image: QLabel):
        """Обновить изображение ОП из массива 288x1."""
        width, height = 1, 288

        image = QImage(width, height, QImage.Format.Format_RGB888)
        image.fill(Qt.GlobalColor.black)

        for y in range(height):
            if op_data[y] == 1:
                for x in range(width):
                    image.setPixelColor(x, y, Qt.GlobalColor.green)

        image = image.mirrored(vertical=True)
        pixmap = QPixmap.fromImage(image)

        op_image.setPixmap(pixmap)

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
