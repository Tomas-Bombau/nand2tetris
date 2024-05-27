import re
import string
import os

class JackTokenizer:
    def __init__(self, file):
        self.filePath = file
        self.title = file.split("/")[-1]
        self.list = []
        self.keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
        self.symbols = ['{','}','[',']','(',')','.',',',';','+','-','*','/','&','|','<','>','=','~']
        self.actualToken = 0
        self.allTokens()

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
                self.list.extend(token for token in tokens if token.strip())

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
        elif actualToken.isdigit():
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
        return f"<integerConstant> {token} </integerConstant>"

    def stringVal(self, token):
        return f"<stringConstant> {token} </stringConstant>"
    
    def identifier(self, token):
        return f"<identifier> {token} </identifier>"
    
    def allTokens(self):
        self.read()
        while self.hasMoreTokens():
            token = self.list[self.actualToken]
            tokenType = self.tokenType()
            if tokenType == "KEYWORD":
                self.keyword(token)
            elif tokenType == "SYMBOL":
                if token == "<":
                    self.symbol("&lt;")
                elif token == ">":
                    self.symbol("&gt;")
                elif token == "\"":
                    self.symbol("&quot;")
                elif token == "&":
                    self.symbol("&amp;")
                else:
                    self.symbol(token)
            elif tokenType == "INT_CONST":
                self.intVal(token)
            elif tokenType == "STRING_CONST":
                token = token.replace("\"","")
                self.stringVal(token)
            elif tokenType == "IDENTIFIER":
                self.identifier(token)
            self.advance()
    
