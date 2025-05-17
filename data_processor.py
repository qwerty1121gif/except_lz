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

# Исключение при ошибках валидации данных
class DataValidationError(DataProcessingError):
    pass

class DataProcessor:
    # Заголовки столбцов для валидации
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
            cls._validate_data(data[1])        # Валидация типов данных в строках
            print("Файл успешно обработан. Структура соответствует требованиям.")
            return True
        except DataProcessingError as e:
            print(f"Ошибка обработки данных: {str(e)}")
            return False

    @classmethod
    def _check_file_exists(cls, filename):
        # Проверка существования файла и его типа
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

        # Валидация структуры данных:
        # - Сравнение количества столбцов
        # - Проверка соответствия названий заголовков

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
            
    @classmethod
    def _validate_data(cls, rows):
        # Валидация типов данных в строках
        for row_num, row in enumerate(rows, start=2):  # Начинаем с 2, т.к. 1 — заголовки
            try:
                float(row[2].strip().replace(',', '.'))  # Проверка записи
            except ValueError:
                raise DataValidationError(f"Некорректный тип данных в строке {row_num}, столбец 'Сумма операции'")
            try:
                float(row[10].strip().replace(',', '.'))  # Проверка 'Сумма cash-back'
            except ValueError:
                raise DataValidationError(f"Некорректный тип данных в строке {row_num}, столбец 'Сумма cash-back'")