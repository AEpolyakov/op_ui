from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel


class OpImageWriter:

    @staticmethod
    def rewrite_op_image(op_data: list[int], op_image: QLabel):
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
    def refine_op_data(buffer: dict[int, int], start_index: int, stop_index: int) -> list[int]:
        """Преобразовать буфер полученный из оп размера 18x16 в одномерный массив размера 288x1"""
        op_words = [buffer[key] for key in range(start_index, stop_index + 1)]
        op_data = []
        for word in op_words:
            temp = word
            for bit in range(16):
                op_data.append(temp & 1)
                temp = temp >> 1
        return op_data

    @staticmethod
    def refine_acps_data(buffer: dict[int, int], start_index: int, stop_index: int) -> list[int]:
        data_words = [buffer[key] for key in range(start_index, stop_index + 1)]
        return data_words

    @staticmethod
    def rewrite_acps_image(data: list[int], label: QLabel) -> None:
        scale = 4
        width, height = 1024 // scale, 1024 // scale

        center = 512 // scale
        offset = 8 // scale
        l_limit = center - offset
        h_limit = center + offset

        pointer_x, pointer_y = data[0] // scale, data[1] // scale

        mark_size = 8 // scale

        image = QImage(width, height, QImage.Format.Format_RGB888)
        image.fill(Qt.GlobalColor.black)

        # Серая сетка
        for y in range(height):
            for x in range(width):
                if x == center or y == center:
                    image.setPixelColor(x, y, Qt.GlobalColor.gray)

        mark_color = Qt.GlobalColor.green if l_limit <= pointer_x <= h_limit and l_limit <= pointer_y <= h_limit else Qt.GlobalColor.red

        # Метка
        for y in range(height):
            for x in range(width):
                if (pointer_x - mark_size <= x <= pointer_x + mark_size and
                        pointer_y - mark_size <= y <= pointer_y + mark_size):
                    # Если в границах - зеленая, иначе красная
                    image.setPixelColor(x, y, mark_color)

        pixmap = QPixmap.fromImage(image)
        label.setPixmap(pixmap)
