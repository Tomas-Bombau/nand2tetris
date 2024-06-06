from VMWriter import VMWriter
from SymbolTable import SymbolTable

class CompilationEngine:
    def __init__(self, tokenizer, outputFile):
        self.tokenizer = tokenizer
        self.outputFile = VMWriter(outputFile)
        self.symbolTable = SymbolTable()
        self.className = ""
        self.subroutineName = ""
        self.subroutineTypeOrClassName = ""
        self.opList = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

    def CompileClass(self):
        self.tokenizer.advance() # get class Name
        self.className = self.tokenizer.actualToken
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()  # get "Global vars" or subroutines
            while self.tokenizer.actualToken == "static" or self.tokenizer.actualToken == "field":
                self.CompileClassVarDec()
                self.tokenizer.advance() # move to subroutine type / 'constructor' or 'method' or 'function'
            while self.tokenizer.actualToken == "method" or self.tokenizer.actualToken == "constructor" or self.tokenizer.actualToken == "function":
                self.CompileSubroutineDec()
                self.tokenizer.advance() 
        print("GLOBAL:", self.symbolTable.globalScope)
        print("SUBROUTINE:",self.symbolTable.subroutineScope)
        self.outputFile.close()

    def CompileClassVarDec(self):
        kind = self.tokenizer.actualToken
        self.tokenizer.advance()
        type = self.tokenizer.actualToken
        self.tokenizer.advance()
        name = self.tokenizer.actualToken
        self.tokenizer.advance()
        self.symbolTable.define(name, type, kind)
        while self.tokenizer.actualToken == ",":
            self.tokenizer.advance()
            name = self.tokenizer.actualToken
            self.symbolTable.define(name, type, kind)
            self.tokenizer.advance()

    def CompileSubroutineDec(self):
        subroutineType = self.tokenizer.actualToken #METHOD, FUNCTION OR CONSTRUCTOR
        self.tokenizer.advance()  # get subroutine type or name
        self.subroutineTypeOrClassName = self.tokenizer.actualToken
        self.tokenizer.advance()  # get subroutine type or name
        self.subroutineName = self.tokenizer.actualToken
        self.symbolTable.startSubroutine() # Clean symbol table
        self.tokenizer.advance()  # move to '(' symbol
        self.compileParameterList(subroutineType)
        self.tokenizer.advance()  # move to '{' symbol
        self.compileSubroutineBody(subroutineType)

    def compileParameterList(self, subroutineType):
        self.tokenizer.advance()
        if self.tokenizer.actualToken == ")":
            return
        else:
            while True:
                if subroutineType == "method":
                    self.symbolTable.define("this", self.className, 'arg') #! A CHEQUEAR
                else:
                    type = self.tokenizer.actualToken
                    self.tokenizer.advance()  # move to argument name
                    name = self.tokenizer.actualToken
                    self.symbolTable.define(name, type, "arg")
                    self.tokenizer.advance()  # move past ',' or ')'
                    if self.tokenizer.actualToken != ",":
                        break
                    else:
                        self.tokenizer.advance()

    def compileSubroutineBody(self, subroutineType):
        self.tokenizer.advance()
        while self.tokenizer.actualToken == "var":
            self.compileVarDec()
        nVars = self.symbolTable.VarCount('var')
        functionName = f"{self.className}.{self.subroutineName}"
        self.outputFile.writeFunction(functionName, nVars)
        if subroutineType == "constructor":
            nFields = self.symbolTable.VarCount('field')
            self.outputFile.WritePush("constant", nFields)
            self.outputFile.WriteCall("Memory.alloc", 1)
            self.outputFile.WritePop("pointer", 0)
        elif subroutineType == "method":
            self.outputFile.WritePush("argument", 0)
            self.outputFile.WritePop("pointer", 0)
        self.compileStatements()

    def compileVarDec(self):
        self.tokenizer.advance()
        type = self.tokenizer.actualToken
        while True:
            self.tokenizer.advance()
            name = self.tokenizer.actualToken
            self.symbolTable.define(name, type, "var")
            self.tokenizer.advance()
            if self.tokenizer.actualToken != ",":
                self.tokenizer.advance()
                break

    def compileStatements(self):
        while self.tokenizer.tokenType() == "KEYWORD":
            if self.tokenizer.actualToken == "let":
                self.compileLet()
            elif self.tokenizer.actualToken== "if":
                self.compileIf()
            elif self.tokenizer.actualToken == "while":
                self.compileWhile()
            elif self.tokenizer.actualToken == "do":
                self.compileDo()
            elif self.tokenizer.actualToken == "return":
                self.compileReturn()

    def compileLet(self):
        isArray = False
        self.tokenizer.advance()
        name = self.tokenizer.actualToken
        self.tokenizer.advance()
        if self.tokenizer.actualToken == "[":  # case of varName[expression]
            isArray = True
            self.compileArrayIndex(name)
        self.tokenizer.advance() 
        self.CompileExpression()
        if isArray:
            self.outputFile.writePop("temp", 0)
            self.outputFile.writePop("pointer", 1)
            self.outputFile.writePush("temp", 0)
            self.outputFile.writePop("that", 0)
        else:
            if self.symbolTable.KindOf(name) == "var":
                segment = "local"
            else:
                segment = "arg"
            index = self.symbolTable.IndexOf(name)
            self.outputFile.WritePop(segment, index)

    # def compileIf(self):
    #     self.outputFile.write("  " * self.indentation + "<ifStatement>\n")
    #     self.indentation += 1
    #     #WRITE IF
    #     self.writeKeyword()
    #     #WRITE "("
    #     self.writeSymbol()
    #     #WRITE EXPRESSION
    #     self.CompileExpression()
    #     #WRITE ")"
    #     self.writeSymbol()
    #     #WRITE "{"
    #     self.writeSymbol()
    #     #WRITE COMPILESTATEMENTS
    #     self.compileStatements()
    #     #WRITE "}"
    #     self.writeSymbol()
    #     #WRITE CONDITIONAL ELSE
    #     if self.tokenizer.actualToken == "else":
    #         #WRITE ELSE
    #         self.writeKeyword()
    #         #WRITE "{"
    #         self.writeSymbol()
    #         #WRITE COMPILESTATEMENTS
    #         self.compileStatements()
    #         #WRITE "}"
    #         self.writeSymbol()
    #     self.indentation -= 1
    #     self.outputFile.write("  " * self.indentation + "</ifStatement>\n")

    # def compileWhile(self):
    #     self.outputFile.write("  " * self.indentation + "<whileStatement>\n")
    #     self.indentation += 1
    #     #WRITE WHILE
    #     self.writeKeyword()
    #     #WRITE "("
    #     self.writeSymbol()
    #     #WRITE EXPRESSION
    #     self.CompileExpression()
    #     #WRITE ")"
    #     self.writeSymbol()
    #     #WRITE "{"
    #     self.writeSymbol()
    #     #WRITE STATEMENTS
    #     self.compileStatements()
    #     #WRITE "}"
    #     self.writeSymbol()
    #     self.indentation -= 1
    #     self.outputFile.write("  " * self.indentation + "</whileStatement>\n")

    def compileDo(self):
        self.tokenizer.advance()
        self.compileSubroutineCall()
        self.outputFile.WritePop('temp', 0)
        self.tokenizer.advance()

    def compileSubroutineCall(self):
        name = lastName = fullName = ''
        nLocals = 0
        name = self.tokenizer.actualToken  # get class/subroutine/var name
        self.tokenizer.advance()
        if self.tokenizer.actualToken == ".":  # case of className.subroutineName
            self.tokenizer.advance() 
            lastName = self.tokenizer.actualToken  # get subroutine name
            if name in self.symbolTable.globalScope or name in self.symbolTable.subroutineScope:
                self.outputFile.writePush(name, lastName)
                fullName = self.symbolTable.typeOf(name) + '.' + lastName
                nLocals += 1
            else:
                fullName = name + '.' + lastName
        else: 
            self.outputFile.WritePush('pointer', 0)
            nLocals += 1
            fullName = self.className + '.' + name
        self.tokenizer.advance()
        nLocals += self.CompileExpressionList()
        self.outputFile.writeCall(fullName, nLocals)
        self.tokenizer.advance()

    def compileReturn(self):
        while self.tokenizer.tokenType() != "SYMBOL":
            self.CompileExpression()
        if self.subroutineTypeOrClassName:
            self.outputFile.WritePush('constant', 0)
            self.subroutineTypeOrClassName = ""
        self.outputFile.writeReturn()       

    def CompileExpression(self):
        self.CompileTerm()
        self.tokenizer.advance()
        while self.tokenizer.actualToken in self.opList:
            op = self.tokenizer.actualToken
            self.tokenizer.advance()
            self.CompileTerm()
            self.tokenizer.advance()
            if op == '+':
                self.outputFile.WriteArithmetic('add')
            elif op == '-':
                self.outputFile.WriteArithmetic('sub')
            elif op == '*':
                self.outputFile.writeCall('Math.multiply', 2)
            elif op == '/':
                self.outputFile.writeCall('Math.divide', 2)
            elif op == '|':
                self.outputFile.WriteArithmetic('or')
            elif op == '&':
                self.outputFile.WriteArithmetic('and')
            elif op == '=':
                self.outputFile.WriteArithmetic('eq')
            elif op == '<':
                self.outputFile.WriteArithmetic('lt')
            elif op == '>':
                self.outputFile.WriteArithmetic('gt')

    def CompileExpressionList(self):
        counter = 0
        self.tokenizer.advance()
        if self.tokenizer.actualToken != ")":
            self.CompileExpression()
            counter += 1
            while self.tokenizer.actualToken == ",":
                self.tokenizer.advance()
                self.CompileExpression()
                counter += 1
        return counter
        
    def CompileTerm(self):
        #INTEGER CONSTANT
        array = False
        if self.tokenizer.tokenType() == "INT_CONST":
            self.outputFile.WritePush("constant", self.tokenizer.actualToken)
        # #STRING CONSTANT
        # elif self.tokenizer.tokenType() == "STRING_CONST":
        #     self.writeStrConst()
        # #KEYWORD CONSTANT
        # elif self.tokenizer.tokenType() == "KEYWORD":
        #     self.writeKeyword()
        # #VARNAME
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            nLocals = 0
            name = self.tokenizer.actualToken  # get class/var/func name
            self.tokenizer.advance()
            #VARNAME[ARRAY]
            if self.tokenizer.actualToken == "[":
                array = True
                self.compileArrayIndex(name)
            #SUBROUTINECALL
            elif self.tokenizer.actualToken == ".":
                self.tokenizer.advance() 
                lastName = self.tokenizer.actualToken  # get subroutine name
                if name in self.symbolTable.globalScope or name in self.symbolTable.subroutineScope:
                    self.outputFile.writePush(name, lastName)
                    name = self.symbolTable.typeOf(name) + '.' + lastName
                    nLocals += 1
                else:
                    name = name + '.' + lastName
                self.tokenizer.advance()  # get '(' symbol
                nLocals += self.CompileExpressionList()
                self.outputFile.writeCall(name, nLocals)
                self.tokenizer.advance()
            #SUBROUTINECALL
            elif self.tokenizer.actualToken == "(":
                nLocals += 1
                self.outputFile.writePush('pointer', 0)
                self.tokenizer.advance()  # get '(' symbol
                nLocals += self.CompileExpressionList()
                self.outputFile.writeCall(self.className + '.' + name, nLocals)
            else:
                if array:
                    self.outputFile.WritePopritePop('pointer', 1)
                    self.outputFile.WritePush('that', 0)
                elif name in self.symbolTable.subroutineScope:
                    if self.symbolTable.KindOf(name) == 'var':
                        self.outputFile.WritePush('local', self.symbolTable.IndexOf(name))
                    elif self.symbolTable.KindOf(name) == 'arg':
                        self.outputFile.WritePush('argument', self.symbolTable.IndexOf(name))
                    self.tokenizer.goBack()
                else:
                    if self.symbolTable.KindOf(name) == 'static':
                        self.outputFile.WritePush('static', self.symbolTable.IndexOf(name))
                    else:
                        self.outputFile.WritePush('this', self.symbolTable.IndexOf(name))
        #EXPRESSION
        elif self.tokenizer.tokenType() == "SYMBOL" and self.tokenizer.actualToken == "(":
            self.tokenizer.advance()
            self.CompileExpression()
        #UNARYOP
        elif self.tokenizer.actualToken == "~" or self.tokenizer.actualToken == "-":
            op = self.tokenizer.actualToken
            self.tokenizer.advance()
            self.CompileTerm()
            if op == '-':
                self.outputFile.WriteArithmetic('neg')
            elif op == '~':
                self.outputFile.WriteArithmetic('not')

