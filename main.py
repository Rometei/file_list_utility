import argparse
from pathlib import Path
import zlib


class FileCreator:

    def __init__(self, default_output_path=None):
        self.files = {}
        self.output_path = default_output_path
        self.running = True
    
    def show_help(self):
        print("""
Доступные команды:
/add <путь_к_файлу>                 - добавить один файл
/adddir <путь_к_директории> [-r]    - добавить директорию рекурсивно или нерекурсивно
/remove <путь_к_файлу>              - удалить один файл
/setpath [путь_к_списку]            - задать путь для сохранения списка             
/save                               - сохранить список
/help                               - вывести список доступных команд
/exit                               - выход из программы
        """)
    
    @staticmethod
    def calculate_crc32(file_path):
        if not file_path.is_file():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        crc = 0
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                crc = zlib.crc32(chunk, crc)
        return format(crc & 0xFFFFFFFF, '08x')

    def add_single_file(self, file_path):
        path = Path(file_path).resolve()
        try:
            crc = self.calculate_crc32(path)
            self.files[str(path)] = crc
            print(f"Добавлен: {path} (crc32: {crc})")
        except Exception as e:
            print(f"Ошибка {e}")     
    
    def process_command(self, line):
        line = line.strip()
        if not line:
            return
        if not line.startswith('/'):
            print("Неизвестная команда.")
            return
        
        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == '/help':
            self.show_help()
        elif cmd == '/exit':
            self.running = False
            print('Выход из программы.')
        elif cmd == '/add':
            if len(args) != 1:
                print("Неправильное кол-во аргументов")
            else:
                self.add_single_file(args[0])
        else:
            print('Неизвестная команда')
    
    def run(self):
        print("Введите /help.")
        while self.running:
            try:
                user_input = input("> ")
                self.process_command(user_input)
            except KeyboardInterrupt:
                print("\nПрерывание программы.")
                self.running = False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o", help="Путь к файлу по умолчанию")
    args = parser.parse_args()
    if args.output:
        default_path = Path(args.output).resolve()
    else:
        default_path = None
    app = FileCreator(default_output_path=default_path)
    app.run()

if __name__ == "__main__":
    main()