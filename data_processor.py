import csv
import os

class DataProcessingError(Exception):
    pass

class FileNotFoundError(DataProcessingError):
    pass

class EmptyFileError(DataProcessingError):
    pass

class InvalidFormatError(DataProcessingError):
    pass

class StructureMismatchError(DataProcessingError):
    pass

class DataProcessor:
    EXPECTED_HEADERS = [
        'Участники гражданского оборота', 'Тип операции', 'Сумма операции',
        'Вид расчета', 'Место оплаты', 'Терминал оплаты', 'Дата оплаты',
        'Время оплаты', 'Результат операции', 'Cash-back', 'Сумма cash-back'
    ]

    @classmethod
    def process_data(cls, filename):
        try:
            cls._check_file_exists(filename)
            data = cls._read_file(filename)
            cls._validate_structure(data)
            print("Файл успешно обработан. Структура соответствует требованиям.")
            return True
        except DataProcessingError as e:
            print(f"Ошибка обработки данных: {str(e)}")
            return False

    @classmethod
    def _check_file_exists(cls, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден")
        if not os.path.isfile(filename):
            raise InvalidFormatError(f"{filename} не является файлом")

    @classmethod
    def _read_file(cls, filename):
        try:
            with open(filename, 'r', encoding='utf-8-sig') as file:
                reader = csv.reader(file, delimiter=',')
                headers = next(reader, None)
                data = list(reader)
                
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
        headers, _ = data
        if len(headers) != len(cls.EXPECTED_HEADERS):
            raise StructureMismatchError(
                f"Несоответствие количества столбцов. Ожидалось: {len(cls.EXPECTED_HEADERS)}, получено: {len(headers)}"
            )
        
        for expected, actual in zip(cls.EXPECTED_HEADERS, headers):
            if expected != actual:
                raise StructureMismatchError(
                    f"Несоответствие структуры. Ожидался столбец: '{expected}', получен: '{actual}'"
                )