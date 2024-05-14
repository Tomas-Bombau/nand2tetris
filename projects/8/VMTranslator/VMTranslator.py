import argparse
import os
from Parser import Parser
from CodeWriter import CodeWriter

class VMTranslator():
    def __init__(self, file_path):
        if os.path.isfile(file_path):
            self.translate_file(file_path, os.path.dirname(file_path))

        elif os.path.isdir(file_path):
            for filename in os.listdir(file_path):
                if filename.endswith(".vm"):
                    self.translate_file(os.path.join(file_path, filename), file_path)
                    
        else:
            raise Exception("Neither a .vm file nor a directory containing .vm files")

    def translate_file(self, input_file, output_dir):
        # Parse commands
        parser = Parser(input_file)
        file_title = parser.title()
        file_parsed = parser.process_commands()
        output_file = os.path.join(output_dir, file_title)

        # Write assembly language
        writer = CodeWriter(output_file)
        writer.clear()
        writer.write_file(file_parsed)
        writer.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate a Python file or directory to ASM language.')
    parser.add_argument('file', help='The file or directory to translate')
    args = parser.parse_args().file
    VMTranslator(args)
