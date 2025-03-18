def refine_buffer(raw_buffer: dict[int, str], buffer_len: int) -> dict[int, int]:
    """Преобразование списка 74x8 бит в словарь 36x16"""
    refined_buffer = dict()

    for index in range(buffer_len // 2):
        refined_buffer[index] = int(raw_buffer[index * 2 + 1] + raw_buffer[index * 2], 16)

    return refined_buffer


def get_bit_value(temp: int, bit: int) -> str:
    """Получение значения конкретного бита из слова."""
    return bin((temp >> bit) & 1)[2:]


def get_bits_value(temp: int, start_bit: int, n_bits: int) -> str:
    """Получение значения нескольких последовательных битов из слова."""
    mask = pow(2, n_bits) - 1
    return f'{bin((temp >> start_bit) & mask)[2:]:0>{n_bits}}'


def convert_input_to_buffer(data: int) -> tuple[int, int]:
    """Преобразовать данные из поля ввода в буфер uart."""
    return data & 0xff, data >> 8
