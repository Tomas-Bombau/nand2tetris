import argparse
from JackTokenizer import JackTokenizer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='JackCompiler', description='Compiler')
    parser.add_argument('filename')
    path = parser.parse_args().filename
    if path.endswith(".jack"):
        newFile = JackTokenizer(path)
    else:
        print("DIRECTORIO")