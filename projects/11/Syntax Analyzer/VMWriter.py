class VMWriter:
    def __init__(self, outputFile):
        self.outputFile = open(outputFile, "a")

    def WritePush(self, segment, index):
        self.outputFile.write(f"push {segment} {index}\n")

    def WritePop(self, segment, index):
        self.outputFile.write(f"pop {segment} {index}\n")

    def WriteArithmetic(self, command):
        self.outputFile.write(f"{command}\n")

    def WriteLabel(self, label):
        self.outputFile.write(f"label {label}\n")

    def WriteGoTo(self, label):
        self.outputFile.write(f"goto{label}\n")

    def WriteIf(self, label):
        self.outputFile.write(f"if-goto{label}\n")

    def writeCall(self, name, nArgs):
        self.outputFile.write(f"call {name} {nArgs}\n")

    def writeFunction(self, name, nLocals):
        self.outputFile.write(f"function {name} {nLocals}\n")

    def writeReturn(self):
        self.outputFile.write("return\n")

    def close(self):
        self.outputFile.close()