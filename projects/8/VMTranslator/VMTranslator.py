import argparse
import os
from Parser import Parser
from CodeWriter import CodeWriter

class VMTranslator():
    def __init__(self, file_path):
        self.directory_name = os.path.basename(os.path.normpath(file_path))
        self.asm_file_path = os.path.join(file_path, f"{self.directory_name}")
        self.CodeWriter = CodeWriter(self.asm_file_path)
    
        if os.path.isfile(file_path):
            self.translate_file(file_path, os.path.dirname(file_path))


        elif os.path.isdir(file_path):
            count = 0
            for filename in os.listdir(file_path):
                if filename.endswith(".vm"):
                    count += 1
            if count > 1:
                self.CodeWriter.setFile()
            for filename in os.listdir(file_path):
                if count == 1 and filename.endswith(".vm"):
                    self.translate_file(os.path.join(file_path, filename), self.asm_file_path)

    def translate_file(self, input_file):
        parser = Parser(input_file)
        file_parsed = parser.process_commands()
        self.CodeWriter.write_file(file_parsed)
        self.CodeWriter.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate a Python file or directory to ASM language.')
    parser.add_argument('file', help='The file or directory to translate')
    args = parser.parse_args().file
    VMTranslator(args)
