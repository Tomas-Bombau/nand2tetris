import argparse
from Parser import Parser
from CodeWriter import CodeWriter


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate a Python file.')
    parser.add_argument('file', help='The file to translate')
    args = parser.parse_args()
    filename = args.file

    file = Parser(filename)
    file_title = file.title()
    file_commands = file.read_vm_file()
    file_parsed = file.process_commands()

    writer = CodeWriter(file_title)
    writer.clear()
    writer.write_file(file_parsed)
    writer.close()


