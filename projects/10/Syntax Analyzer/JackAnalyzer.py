import argparse
import os
from pathlib import Path
from JackTokenizer import JackTokenizer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='JackCompiler', description='Compiler')
    parser.add_argument('filename')
    path = parser.parse_args().filename
    if path.endswith(".jack"):
        JackTokenizer(path)
    else:
        for jackFiles in os.listdir(path):
            if jackFiles.endswith(".jack"):
                full_path = os.path.join(path, jackFiles)
                JackTokenizer(full_path)