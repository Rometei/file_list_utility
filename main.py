import argparse
from pathlib import Path


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