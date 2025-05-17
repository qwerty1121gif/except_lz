import csv
import os

# Базовое исключение для ошибок обработки данных
class DataProcessingError(Exception):
    pass

# Исключение при отсутствии файла
class FileNotFoundError(DataProcessingError):
    pass

# Исключение при пустом файле
class EmptyFileError(DataProcessingError):
    pass

# Исключение при неверном формате файла
class InvalidFormatError(DataProcessingError):
    pass

# Исключение при несоответствии структуры данных
class StructureMismatchError(DataProcessingError):
    pass

class DataProcessor:
    # Pаголовки столбцов для валидации
    EXPECTED_HEADERS = [
        'Участники гражданского оборота', 'Тип операции', 'Сумма операции',
        'Вид расчета', 'Место оплаты', 'Терминал оплаты', 'Дата оплаты',
        'Время оплаты', 'Результат операции', 'Cash-back', 'Сумма cash-back'
    ]

    @classmethod
    def process_data(cls, filename):

        # Основной метод обработки данных.
        # Выполняет последовательность проверок и валидаций.
        # Возвращает True при успешной обработке, False при ошибках.

        try:
            cls._check_file_exists(filename)   # Проверка существования файла
            data = cls._read_file(filename)    # Чтение данных из файла
            cls._validate_structure(data)      # Валидация структуры данных
            print("Файл успешно обработан. Структура соответствует требованиям.")
            return True
        except DataProcessingError as e:
            print(f"Ошибка обработки данных: {str(e)}")
            return False

    @classmethod
    def _check_file_exists(cls, filename):
        # Проверка существования файла и его типа (регулярный файл)
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден")
        if not os.path.isfile(filename):
            raise InvalidFormatError(f"{filename} не является файлом")

    @classmethod
    def _read_file(cls, filename):

        # Чтение CSV файла и извлечение данных
        # Возвращает кортеж
        # Обрабатывает ошибки чтения и декодирования

        try:
            with open(filename, 'r', encoding='utf-8-sig') as file:
                reader = csv.reader(file, delimiter=',')
                headers = next(reader, None)  # Чтение заголовков
                data = list(reader)           # Чтение остальных данных

                # Проверки на пустой файл
                if not headers:
                    raise EmptyFileError("Файл пуст")
                if not data:
                    raise EmptyFileError("Файл содержит только заголовки")

                return headers, data
        except UnicodeDecodeError:
            raise InvalidFormatError("Некорректная кодировка файла")
        except csv.Error:
            raise InvalidFormatError("Ошибка чтения CSV файла")

    @classmethod
    def _validate_structure(cls, data):
        """
        Валидация структуры данных:
        - Сравнение количества столбцов
        - Проверка соответствия названий заголовков
        """
        headers, _ = data
        # Проверка количества столбцов
        if len(headers) != len(cls.EXPECTED_HEADERS):
            raise StructureMismatchError(
                f"Несоответствие количества столбцов. Ожидалось: {len(cls.EXPECTED_HEADERS)}, получено: {len(headers)}"
            )

        # Построчная проверка названий столбцов
        for expected, actual in zip(cls.EXPECTED_HEADERS, headers):
            if expected != actual:
                raise StructureMismatchError(
                    f"Несоответствие структуры. Ожидался столбец: '{expected}', получен: '{actual}'"
                )