from data_processor import DataProcessor

def main():
    filename = "var5.csv"
    if DataProcessor.process_data(filename):
        # Дальнейшая обработка данных
        pass
    else:
        print("Обработка файла прервана из-за ошибок")

if __name__ == "__main__":
    main()