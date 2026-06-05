class File:
    def __init__(self, name):
        self.name = name
        self.content = ""

    def write(self, text):
        self.content = text

    def read(self):
        return self.content

    def get_name(self):
        return self.name

class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.subdirectories = {}
        self.files = {}

    def create_directory(self, path):
        parts = path.split('/', 1)
        dir_name = parts[0]

        if dir_name in self.subdirectories:
            if len(parts) > 1:
                return self.subdirectories[dir_name].create_directory(parts[1])
            return self.subdirectories[dir_name]
        else:
            new_dir = Directory(dir_name, self)
            self.subdirectories[dir_name] = new_dir
            if len(parts) > 1:
                return new_dir.create_directory(parts[1])
            return new_dir

    def get_directory(self, path):
        if path == "" or path == ".":
            return self

        parts = path.split('/', 1)
        dir_name = parts[0]

        if dir_name == "..":
            return self.parent if self.parent else self

        if dir_name in self.subdirectories:
            if len(parts) > 1:
                return self.subdirectories[dir_name].get_directory(parts[1])
            return self.subdirectories[dir_name]
        return None

    def create_file(self, path):
        parts = path.rsplit('/', 1)

        if len(parts) == 1:
            dir_path = ""
            file_name = parts[0]
        else:
            dir_path = parts[0]
            file_name = parts[1]

        if dir_path == "":
            target_dir = self
        else:
            target_dir = self.get_directory(dir_path)
            if target_dir is None:
                return None

        if file_name not in target_dir.files:
            target_dir.files[file_name] = File(file_name)

        return target_dir.files[file_name]

    def get_file(self, path):
        parts = path.rsplit('/', 1)

        if len(parts) == 1:
            dir_path = ""
            file_name = parts[0]
        else:
            dir_path = parts[0]
            file_name = parts[1]

        if dir_path == "":
            target_dir = self
        else:
            target_dir = self.get_directory(dir_path)
            if target_dir is None:
                return None

        if file_name in target_dir.files:
            return target_dir.files[file_name]
        return None

    def list_contents(self):
        contents = {
            'directories': list(self.subdirectories.keys()),
            'files': list(self.files.keys())
        }
        return contents

    def get_name(self):
        return self.name

class FileSystem:
    def __init__(self):
        self.root = Directory("")
        self.current_dir = self.root

    def mkdir(self, path):
        return self.root.create_directory(path)

    def cd(self, path):
        new_dir = self.root.get_directory(path)
        if new_dir:
            self.current_dir = new_dir
            return True
        return False

    def pwd(self):
        path_parts = []
        current = self.current_dir
        while current.parent is not None:
            path_parts.append(current.name)
            current = current.parent
        path_parts.reverse()
        return '/' + '/'.join(path_parts) if path_parts else '/'

    def write_file(self, path, content):
        file_obj = self.root.create_file(path)
        if file_obj:
            file_obj.write(content)
            return True
        return False

    def read_file(self, path):
        file_obj = self.root.get_file(path)
        if file_obj:
            return file_obj.read()
        return None

    def list_dir(self, path=""):
        if path == "":
            target_dir = self.current_dir
        else:
            target_dir = self.root.get_directory(path)

        if target_dir:
            return target_dir.list_contents()
        return None

def main():
    fs = FileSystem()

    print("=" * 50)
    print("ФАЙЛОВАЯ СИСТЕМА")
    print("=" * 50)
    print("\nДоступные команды:")
    print("mkdir <path>     - создать директорию")
    print("cd <path>        - перейти в директорию")
    print("pwd              - показать текущую директорию")
    print("ls [path]        - показать содержимое директории")
    print("write <path>     - записать в файл")
    print("read <path>      - прочитать файл")
    print("exit             - выход")
    print("=" * 50)

    while True:
        print(f"\n{fs.pwd()}>", end=" ")
        command = input().strip().split()

        if not command:
            continue

        cmd = command[0].lower()

        if cmd == "exit":
            print("Выход из программы")
            break

        elif cmd == "mkdir":
            if len(command) < 2:
                print("Ошибка: укажите путь к директории")
            else:
                path = command[1]
                fs.mkdir(path)
                print(f"Директория '{path}' создана")

        elif cmd == "cd":
            if len(command) < 2:
                print("Ошибка: укажите путь")
            else:
                path = command[1]
                if fs.cd(path):
                    print(f"Переход в '{path}' выполнен")
                else:
                    print(f"Ошибка: директория '{path}' не найдена")

        elif cmd == "pwd":
            print(f"Текущая директория: {fs.pwd()}")

        elif cmd == "ls":
            path = command[1] if len(command) > 1 else ""
            contents = fs.list_dir(path)
            if contents:
                display_path = path if path else fs.pwd()
                print(f"\nСодержимое '{display_path}':")
                if contents['directories']:
                    print("  Директории: " + ", ".join(contents['directories']))
                if contents['files']:
                    print("  Файлы: " + ", ".join(contents['files']))
                if not contents['directories'] and not contents['files']:
                    print("  (пусто)")
            else:
                print(f"Ошибка: директория не найдена")

        elif cmd == "write":
            if len(command) < 2:
                print("Ошибка: укажите путь к файлу")
            else:
                path = command[1]
                print("Введите содержимое файла (завершите пустой строкой):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                content = "\n".join(lines)
                if fs.write_file(path, content):
                    print(f"Файл '{path}' записан")
                else:
                    print(f"Ошибка: не удалось создать файл")

        elif cmd == "read":
            if len(command) < 2:
                print("Ошибка: укажите путь к файлу")
            else:
                path = command[1]
                content = fs.read_file(path)
                if content is not None:
                    print(f"\nСодержимое '{path}'")
                    print(content)
                    print("Конец файла")
                else:
                    print(f"Ошибка: файл '{path}' не найден")

        else:
            print(f"Неизвестная команда: {cmd}")

if __name__ == "__main__":
    main()