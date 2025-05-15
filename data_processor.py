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
class DataProcessor():
    EXPECTED_HEADERS = [
        'Участники гражданского оборота', 'Тип операции', 'Сумма операции',
        'Вид расчета', 'Место оплаты', 'Терминал оплаты', 'Дата оплаты',
        'Время оплаты', 'Результат операции', 'Cash-back', 'Сумма cash-back'
    ]
    