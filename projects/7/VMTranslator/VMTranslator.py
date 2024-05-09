import argparse
import os
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file(input_file, output_dir):
    file = Parser(input_file)
    file_title = file.title()
    file_commands = file.read_vm_file()
    file_parsed = file.process_commands()
    output_file = os.path.join(output_dir, file_title)
    writer = CodeWriter(output_file)
    writer.clear()
    writer.write_file(file_parsed)
    writer.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate a Python file or directory.')
    parser.add_argument('file', help='The file or directory to translate')
    args = parser.parse_args()

    if os.path.isfile(args.file):
        translate_file(args.file, os.path.dirname(args.file))

    elif os.path.isdir(args.file):
        for file_name in os.listdir(args.file):
            if file_name.endswith(".vm"):
                input_file = os.path.join(args.file, file_name)
                translate_file(input_file, args.file)
    else:
        raise Exception("Neither a .vm file or a directory containing .vm files")

