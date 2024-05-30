class CompilationEngine:
    def __init__(self, tokenizer, outputFile):
        self.tokenizer = tokenizer
        self.outputFile = open(outputFile, "a")
        self.indentation = 0
        self.opList = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

    def CompileClass(self):
        self.outputFile.write("<class>\n")
        self.indentation += 1
        while self.tokenizer.hasMoreTokens():
            self.writeKeyword()
            self.writeIdentifier()
            self.writeSymbol()
            while self.tokenizer.actualToken == "static" or self.tokenizer.actualToken == "field":
                self.CompileClassVarDec()
            while self.tokenizer.actualToken == "method" or self.tokenizer.actualToken == "constructor" or self.tokenizer.actualToken == "function":
                self.CompileSubroutineDec()
            self.writeSymbol()
        self.indentation -= 1
        self.outputFile.write("</class>\n")
        self.outputFile.close()

    def CompileClassVarDec(self):
        self.outputFile.write("  " * self.indentation + "<classVarDec>\n")
        self.indentation += 1
        self.writeKeyword()
        #TYPE
        if self.tokenizer.tokenType() == "KEYWORD": #SI ES INT, CHAR, BOOLEAN
            self.writeKeyword()
        elif self.tokenizer.tokenType() == "IDENTIFIER": #SI ES UNA CLASSNAME
            self.writeIdentifier()
        #VARNAME or VARNAMES
        self.writeIdentifier()
        while self.tokenizer.actualToken == ",":
            self.writeSymbol()
            self.writeIdentifier()
        self.writeSymbol()
        #WRITE ;
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</classVarDec>\n")

    def CompileSubroutineDec(self):
        self.outputFile.write("  " * self.indentation + "<subroutineDec>\n")
        self.indentation += 1
        self.writeKeyword()
        #VOID OR TYPE
        if self.tokenizer.tokenType() == "KEYWORD":
            self.writeKeyword()
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            self.writeIdentifier()
        #SUBROUTINENAME
        self.writeIdentifier()
        #SYMBOL
        self.writeSymbol()
        #PARAMETERLIST
        self.compileParameterList()
        #SYMBOL
        self.writeSymbol()
        #SUBROUTINEBODY
        self.compileSubroutineBody()
        #WRITE
        self.indentation -= 1
        self.outputFile.write(("  " * self.indentation + "</subroutineDec>\n"))

    def compileParameterList(self):
        self.outputFile.write("  " * self.indentation + "<parameterList>\n")
        self.indentation += 1
        while self.tokenizer.tokenType() != "SYMBOL":
            if  self.tokenizer.tokenType() == "KEYWORD":
                self.writeKeyword()
            elif self.tokenizer.tokenType() == "IDENTIFIER":
                self.writeIdentifier()
            if self.tokenizer.actualToken == ",":
                self.writeSymbol()
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</parameterList>\n")

    def compileSubroutineBody(self):
        self.outputFile.write("  " * self.indentation + "<subroutineBody>\n")
        self.indentation += 1
        #WRITE "{""
        self.writeSymbol()
        #VARDEC O VARDECS
        while self.tokenizer.actualToken == "var":
            self.compileVarDec()
        self.compileStatements()
        #WRITE "}"
        self.writeSymbol()
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</subroutineBody>\n")

    def compileVarDec(self):
        self.outputFile.write("  " * self.indentation + "<varDec>\n")
        self.indentation += 1
        #WRITE VAR
        self.writeKeyword()
        #WRITE TYPE
        if self.tokenizer.tokenType() == "KEYWORD":
                self.writeKeyword()
        elif self.tokenizer.tokenType() == "IDENTIFIER":
                self.writeIdentifier()
        #WRITE VARNAME OR VARNAMES
        self.writeIdentifier()
        while self.tokenizer.actualToken == ",":
            self.writeSymbol()
            self.writeIdentifier()
        #WRITE ;
        self.writeSymbol()
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</varDec>\n")

    def compileStatements(self):
        self.outputFile.write("  " * self.indentation + "<statements>\n")
        self.indentation += 1
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
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</statements>\n")

    def compileLet(self):
        self.outputFile.write("  " * self.indentation + "<letStatement>\n")
        self.indentation += 1
        #WRITE LET
        self.writeKeyword()
        #WRITE VARNAME
        self.writeIdentifier()
        #WRITE CONDITIONAL [
        if self.tokenizer.actualToken == "[":
            self.writeSymbol()
            self.CompileExpression()
            self.writeSymbol()
        #WRITE "=""
        self.writeSymbol()
        #WRITE EXPRESSION
        self.CompileExpression()
        #WRITE ";"
        self.writeSymbol()
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</letStatement>\n")

    def compileIf(self):
        self.outputFile.write("  " * self.indentation + "<ifStatement>\n")
        self.indentation += 1
        #WRITE IF
        self.writeKeyword()
        #WRITE "("
        self.writeSymbol()
        #WRITE EXPRESSION
        self.CompileExpression()
        #WRITE ")"
        self.writeSymbol()
        #WRITE "{"
        self.writeSymbol()
        #WRITE COMPILESTATEMENTS
        self.compileStatements()
        #WRITE "}"
        self.writeSymbol()
        #WRITE CONDITIONAL ELSE
        if self.tokenizer.actualToken == "else":
            #WRITE ELSE
            self.writeKeyword()
            #WRITE "{"
            self.writeSymbol()
            #WRITE COMPILESTATEMENTS
            self.compileStatements()
            #WRITE "}"
            self.writeSymbol()
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</ifStatement>\n")

    def compileWhile(self):
        self.outputFile.write("  " * self.indentation + "<whileStatement>\n")
        self.indentation += 1
        #WRITE WHILE
        self.writeKeyword()
        #WRITE "("
        self.writeSymbol()
        #WRITE EXPRESSION
        self.CompileExpression()
        #WRITE ")"
        self.writeSymbol()
        #WRITE "{"
        self.writeSymbol()
        #WRITE STATEMENTS
        self.compileStatements()
        #WRITE "}"
        self.writeSymbol()
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</whileStatement>\n")

    def compileDo(self):
        self.outputFile.write("  " * self.indentation + "<doStatement>\n")
        self.indentation += 1
        #WRITE DO
        self.writeKeyword()
        #WRITE SUBROUTINECALL
        self.writeIdentifier()
        if self.tokenizer.actualToken == ".":
            self.writeSymbol()
            self.writeIdentifier()
        #WRITE "("
        self.writeSymbol()
        #WRITE EXPRESSION LIST
        self.CompileExpressionList()
        #WRITE ")"
        self.writeSymbol()
        #WRITE ";"
        self.writeSymbol()
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</doStatement>\n")

    def compileReturn(self):
        self.outputFile.write("  " * self.indentation + "<returnStatement>\n")
        self.indentation += 1
        #WRITE RETURN
        self.writeKeyword()
        #WRITE SUBROUTINECALL
        if self.tokenizer.tokenType() != "SYMBOL":
            self.CompileExpression()
        #WRITE ";"
        self.writeSymbol()
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</returnStatement>\n")

    def CompileExpression(self):
        self.outputFile.write("  " * self.indentation + "<expression>\n")
        self.indentation += 1
        self.CompileTerm()
        while self.tokenizer.actualToken in self.opList:
            self.writeSymbol()
            self.CompileTerm()
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</expression>\n")

    def CompileExpressionList(self):
        self.outputFile.write("  " * self.indentation + "<expressionList>\n")
        self.indentation += 1
        if self.tokenizer.actualToken != ")":
            self.CompileExpression()
            while self.tokenizer.actualToken == ",":
                self.writeSymbol()
                self.CompileExpression()
        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</expressionList>\n")

    def CompileTerm(self):
        self.outputFile.write("  " * self.indentation + "<term>\n")
        self.indentation += 1
        #INTEGER CONSTANT
        if self.tokenizer.tokenType() == "INT_CONST":
            self.writeIntConst()
        #STRING CONSTANT
        elif self.tokenizer.tokenType() == "STRING_CONST":
            self.writeStrConst()
        #KEYWORD CONSTANT
        elif self.tokenizer.tokenType() == "KEYWORD":
            self.writeKeyword()
        #VARNAME
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            self.writeIdentifier()
            #VARNAME[ARRAY]
            if self.tokenizer.actualToken == "[":
                self.writeSymbol()
                self.CompileExpression()
                self.writeSymbol()
             #SUBROUTINECALL
            elif self.tokenizer.actualToken == ".":
                self.writeSymbol()
                self.writeIdentifier()
                self.writeSymbol()
                self.CompileExpressionList()
                self.writeSymbol()
             #SUBROUTINECALL
            elif self.tokenizer.actualToken == "(":
                self.writeSymbol()
                self.CompileExpressionList()
                self.writeSymbol()
        #EXPRESSION
        elif self.tokenizer.tokenType() == "SYMBOL" and self.tokenizer.actualToken == "(":
            self.writeSymbol()
            self.CompileExpression()
            self.writeSymbol()
        #UNARYOP
        elif self.tokenizer.actualToken == "~" or self.tokenizer.actualToken == "-":
            self.writeSymbol()
            self.CompileTerm()

        self.indentation -= 1
        self.outputFile.write("  " * self.indentation + "</term>\n")

    def writeIdentifier(self):
        self.outputFile.write("  " * self.indentation + "<identifier> " +  self.tokenizer.actualToken + " </identifier>\n")
        self.tokenizer.advance()

    def writeKeyword(self):
        self.outputFile.write("  " * self.indentation + "<keyword> " +  self.tokenizer.actualToken + " </keyword>\n")
        self.tokenizer.advance()

    def writeSymbol(self):
        if self.tokenizer.actualToken == "<":
            self.tokenizer.actualToken = "&lt;"
        elif self.tokenizer.actualToken == ">":
            self.tokenizer.actualToken = "&gt;"
        elif self.tokenizer.actualToken == "\"":
            self.tokenizer.actualToken = "&quot;;"
        elif self.tokenizer.actualToken == "&":
            self.tokenizer.actualToken = "&amp;"
        self.outputFile.write("  " * self.indentation + "<symbol> " +  self.tokenizer.actualToken + " </symbol>\n")
        self.tokenizer.advance()

    def writeIntConst(self):
        self.outputFile.write("  " * self.indentation + "<integerConstant> " +  self.tokenizer.actualToken + " </integerConstant>\n")
        self.tokenizer.advance()

    def writeStrConst(self):
        self.outputFile.write("  " * self.indentation + "<stringConstant> " +  self.tokenizer.actualToken.replace("\"", "")  + " </stringConstant>\n")
        self.tokenizer.advance()