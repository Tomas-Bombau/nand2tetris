import argparse
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

class Tokenizer():
    def __init__(self):
        self.new = self.tokenizer()

    def tokenizer(self):
        parser = argparse.ArgumentParser(prog='JackCompiler', description='Compiler')
        parser.add_argument('filename', help='Path to .jack file or directory containing .jack files')
        args = parser.parse_args()
        path = args.filename
        if os.path.isfile(path) and path.endswith(".jack"):
            return [self.tokenizeFile(path)]
        elif os.path.isdir(path):
            return self.tokenizeDirectory(path)
        else:
            print("Invalid input. Please provide a .jack file or directory containing .jack files.")

    def tokenizeFile(self, filePath):
        return JackTokenizer(filePath)

    def tokenizeDirectory(self, directoryPath):
        tokenizers = []
        for fileName in os.listdir(directoryPath):
            if fileName.endswith(".jack"):
                fullPath = os.path.join(directoryPath, fileName)
                tokenizers.append(self.tokenizeFile(fullPath))
        return tokenizers

if __name__ == '__main__':
    start = Tokenizer().new
    for tokenizer in start:
        CompilationEngine(tokenizer)


















# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(prog='JackCompiler', description='Compiler')
#     parser.add_argument('filename')
#     path = parser.parse_args().filename
#     if path.endswith(".jack"):
#         JackTokenizer(path)
#     else:
#         for jackFiles in os.listdir(path):
#             if jackFiles.endswith(".jack"):
#                 full_path = os.path.join(path, jackFiles)
#                 JackTokenizer(full_path)