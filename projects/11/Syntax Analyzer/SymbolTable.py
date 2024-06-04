class SymbolTable:
    def __init__(self):
        self.globalScope = {}
        self.subroutineScope = {}
        self.staticCount = 0
        self.fieldCount = 0
        self.argCount = 0
        self.variableCount = 0

    def startSubroutine(self):
        self.subroutineScope = {}
        self.argCount = 0
        self.variableCount = 0

    def define(self, name, type, kind):
        if kind == "static":
            self.globalScope[name] = (type, kind, self.staticCount)
            self.staticCount += 1
        elif kind == "field":
            self.globalScope[name] = (type, kind, self.fieldCount)
            self.fieldCount += 1
        elif kind == "arg":
            self.subroutineScope[name] = (type, kind, self.argCount)
            self.argCount += 1
        elif kind == "var":
            self.subroutineScope[name] = (type, kind, self.variableCount)
            self.variableCount += 1

    def VarCount(self, kind):
        if kind == "static":
            return self.staticCount
        elif kind == "field":
            return self.fieldCount
        if kind == "arg":
            return self.argCount
        if kind == "var":
            return self.variableCount
        
    def KindOf(self, name):
        if name in self.globalScope:
            return self.globalScope.get(name)[1]
        elif name in self.subroutineScope:
            return self.subroutineScope.get(name)[1]
        else:
            return None

    def TypeOf(self, name):
        if name in self.globalScope:
            return self.globalScope.get(name)[0]
        elif name in self.subroutineScope:
            return self.subroutineScope.get(name)[0]
        else:
            return None

    def IndexOf(self, name):
        if name in self.globalScope:
            return self.globalScope.get(name)[2]
        elif name in self.subroutineScope:
            return self.subroutineScope.get(name)[2]
        else:
            return None