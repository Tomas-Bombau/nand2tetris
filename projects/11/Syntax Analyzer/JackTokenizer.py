import re
import string

class JackTokenizer:
    def __init__(self, file):
        self.filePath = file
        self.title = file.split("/")[-1]
        self.keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
        self.symbols = ['{','}','[',']','(',')','.',',',';','+','-','*','/','&','|','<','>','=','~']
        self.tokensFound = []
        self.actualToken = None
        self.tokenIndex = 0
        self.read()

    def read(self):
        with open(self.filePath, "r") as infile:
            in_comment = False
            for line in infile:
                line = line.strip()
                if '/*' in line:
                    in_comment = True
                    if '*/' in line:
                        line = re.sub(r'/\*.*\*/', '', line)
                        in_comment = False
                    else:
                        line = re.sub(r'/\*.*', '', line)
                elif '*/' in line:
                    in_comment = False
                    line = re.sub(r'.*\*/', '', line)
                if in_comment:
                    continue 
                line = re.sub(r"//.*", '', line)
                tokens = re.split(r'(\s+|[()\{\};,.\[\]+\-*/&|<>=~]|"(?:\\.|[^"])*")', line)
                self.tokensFound.extend(token for token in tokens if token.strip())

    def hasMoreTokens(self):
        if self.tokenIndex < len(self.tokensFound):
            self.actualToken = self.tokensFound[self.tokenIndex]
        elif self.tokenIndex >= len(self.tokensFound):
            return False
        return True

    def advance(self):
        self.tokenIndex += 1
        self.hasMoreTokens()

    def goBack(self):
        self.tokenIndex -= 1
        self.hasMoreTokens()

    def tokenType(self):
        if self.actualToken in self.keywords:
            return "KEYWORD"
        elif self.actualToken in self.symbols:
            return "SYMBOL"
        elif self.actualToken.isdigit():
            return "INT_CONST"
        elif self.actualToken.startswith('"'):
            return "STRING_CONST"
        elif any(self.actualToken.startswith(letter) for letter in string.ascii_letters):
            return "IDENTIFIER"

    # def keyword(self, token):
    #     return token
    
    # def symbol(self, token):
    #     return token

    # def intVal(self, token):
    #     return token

    # def stringVal(self, token):
    #     return token
    
    # def identifier(self, token):
    #     return token
    
    # def allTokens(self):
    #     while self.hasMoreTokens():
            # tokenType = self.tokenType()
            # if tokenType == "KEYWORD":
            #     self.keyword(self.actualToken)
            # elif tokenType == "SYMBOL":
            #     if self.actualToken == "<":
            #         self.symbol("&lt;")
            #     elif self.actualToken == ">":
            #         self.symbol("&gt;")
            #     elif self.actualToken == "\"":
            #         self.symbol("&quot;")
            #     elif self.actualToken == "&":
            #         self.symbol("&amp;")
            #     else:
            #         self.symbol(self.actualToken)
            # elif tokenType == "INT_CONST":
            #     self.intVal(self.actualToken)
            # elif tokenType == "STRING_CONST":
            #     token = self.actualToken.replace("\"","")
            #     self.stringVal(token)
            # elif tokenType == "IDENTIFIER":
            #     self.identifier(self.actualToken)
            # self.advance()
