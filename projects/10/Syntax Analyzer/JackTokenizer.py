import re

class JackTokenizer:
    def __init__(self, file):
        self.filePath = file
        self.list = []
        self.keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
        self.symbols = []
        self.actualToken = 0
        self.read()

    def read(self):
        with open(self.filePath, "r") as infile:
            for lines in infile:
                lines = lines.strip()
                lines = re.sub(r"(\/\/.*|\/\*[\s\S]*?\*\/)", '', lines)
                lines = re.sub(r'([()\{\};])', r' \1 ', lines)
                tokens = re.split(r'(\s+|[()\{\};])', lines)
                tokens = [token for token in tokens if token.strip()]
                self.list.extend(tokens)
        print(self.list)

    def hasMoreTokens(self):
        return self.actualToken > len(self.list) - 1
    
    def advance(self):
        if self.HasMoreTokens() == True:
            self.actualToken += 1
        else:
            return
        
    def tokenType(self):
        actualToken = self.list[self.actualToken]
        if actualToken in self.keywords:
            return "KEYWORD"