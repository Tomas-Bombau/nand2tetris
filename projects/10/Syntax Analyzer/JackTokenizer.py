import re
import string

class JackTokenizer:
    def __init__(self, file):
        self.filePath = file
        self.list = []
        self.keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
        self.symbols = ['{','}','[',']','(',')','.',',',';','+','-','*','/','&','|','<','>','=','~']
        self.actualToken = 0
        self.writeXml()

    def read(self):
        with open(self.filePath, "r") as infile:
            for lines in infile:
                lines = lines.strip()
                lines = re.sub(r"(\/\/.*|\/\*[\s\S]*?\*\/)", '', lines)
                lines = re.sub(r'([()\{\};.])', r' \1 ', lines)
                tokens = re.split(r'(\s+|[()\{\};])', lines)
                tokens = [token for token in tokens if token.strip()]
                self.list.extend(tokens)

    def hasMoreTokens(self):
        if self.actualToken > len(self.list) - 1:
            return False
        else:
            return True
    
    def advance(self):
        if self.hasMoreTokens() == True:
            self.actualToken += 1
        else:
            return
        
    def tokenType(self):
        actualToken = self.list[self.actualToken]
        if actualToken in self.keywords:
            return "KEYWORD"
        elif actualToken in self.symbols:
            return "SYMBOL"
        elif actualToken.startswith(string.digits):
            return "INT_CONST"
        elif actualToken.startswith('"'):
            return "STRING_CONST"
        elif (actualToken.startswith(letter) for letter in string.ascii_letters):
            return "IDENTIFIER"
    
    def keyword(self, token):
        return f"<keyword> {token} </keyword>"
    
    def symbol(self, token):
        return f"<symbol> {token} </symbol>"

    def intVal(self, token):
        return f"<intVal> {token} </intVal>"

    def stringVal(self, token):
        return f"<stringVal> {token} </stringVal>"
    
    def identifier(self, token):
        return f"<identifier> {token} </identifier>"
    
    def writeLine(self, input):
        with open(f"PRUEBA.xml", "a") as xmlFile:
            xmlFile.write(f"{input}\n")

    def writeXml(self):
        self.read()
        while self.hasMoreTokens():
            token = self.list[self.actualToken]
            tokenType = self.tokenType()
            if tokenType == "KEYWORD":
                self.writeLine(self.keyword(token))
            elif tokenType == "SYMBOL":
                self.writeLine(self.symbol(token))
            elif tokenType == "INT_CONST":
                self.writeLine(self.intVal(token))
            elif tokenType == "STRING_CONST":
                self.writeLine(self.stringVal(token))
            elif tokenType == "IDENTIFIER":
                self.writeLine(self.identifier(token))
            self.advance()
    
