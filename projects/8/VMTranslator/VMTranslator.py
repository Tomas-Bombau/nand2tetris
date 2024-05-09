import argparse
import os
from Parser import Parser
from CodeWriter import CodeWriter

class VMTranslator():
    def __init__(self, args):
        self.args = args
        self.type_of_file()

    def type_of_file(self):
        if os.path.isfile(self.args):
            output_dir = os.path.dirname(self.args)
            self.translate_file(self.args, output_dir)

        elif os.path.isdir(self.args):
            for file_name in os.listdir(self.args):
                if file_name.endswith(".vm"):
                    input_file = os.path.join(self.args, file_name)
                    output_dir = self.args
                    self.translate_file(input_file, output_dir)
        else:
            raise Exception("Neither a .vm file or a directory containing .vm files")
        
    def translate_file(self, input_file, output_dir):
        #PARSE COMMANDS
        file = Parser(input_file)
        file_title = file.title()
        file.read_vm_file()
        file_parsed = file.process_commands()
        output_file = os.path.join(output_dir, file_title)
        
        #WRITE ASSEMBLY LANGUAGE
        writer = CodeWriter(output_file)
        writer.clear()
        writer.write_file(file_parsed)
        writer.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate a Python file or directory to ASM language.')
    parser.add_argument('file', help='The file or directory to translate')
    args = parser.parse_args().file
    VMTranslator(args)
    

