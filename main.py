import argparse
from pathlib import Path
import zlib
import os


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

    def add_directory(self, args):
        if not args:
            print("Укажите путь")
            return
        dir_path_str = args[0]
        recursive = '-r' in args

        dir_path = Path(dir_path_str).resolve()
        if not dir_path.is_dir():
            print(f"{dir_path} не является директорией.")
            return
        
        files_to_add = []
        if recursive:
            for root, _, files in os.walk(dir_path):
                for file in files:
                    files_to_add.append(Path(root) / file)
        else:
            for item in dir_path.iterdir():
                if item.is_file():
                    files_to_add.append(item)
        
        if not files_to_add:
            print("Нет файлов для добавления")
            return
        
        success = 0
        errors = 0
        for file_path in files_to_add:
            try:
                crc = self.calculate_crc32(file_path)
                self.files[str(file_path)] = crc
                print(f"Добавлен: {file_path} (crc32: {crc})")
                success+=1
            except Exception as e:
                print(f"Не удалось добавить {file_path}: {e}")
                errors+=1
        print(f"Добавлено: {success}, ошибок: {errors}")
    
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
        elif cmd == '/adddir':
            self.add_directory(args)
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