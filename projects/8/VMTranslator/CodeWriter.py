#! CLASS WRITER
import os  
class CodeWriter:
    def __init__(self, output_file):
        self.output_file = output_file
        self.file_title = os.path.basename(output_file).split(".")[0]
        self.label = 0

    def clear(self):
        with open(f"{self.output_file}.asm", 'w'):
            pass

    def setFileName(self):
        pass
    
    def writeInit(self):
        pass

    def writen_format(self, full_command, asm_commands):
        with open(f"{self.output_file}.asm", "a") as asm_file:
            asm_file.write(f"// {full_command}\n")
            for asm_code in asm_commands:
                    asm_file.write(f"{asm_code}\n")

    def write_file(self, parsed_commands):
        for commands in parsed_commands:
            for type_of_command, full_command in commands.items():
                if type_of_command == "CMD_ARITHMETIC":
                    self.writen_format(full_command, self.writeArithmetic(full_command))

                elif type_of_command in ["CMD_PUSH", "CMD_POP"]:
                    action, segment, index = full_command.split(" ")[0:3]
                    self.writen_format(full_command, self.writePushPop(action, segment, index))

                elif type_of_command == "CMD_LABEL":
                    label = full_command.split(" ")[1]
                    self.writen_format(full_command, self.writeLabel(label))

                elif type_of_command == "CMD_GOTO":
                    label = full_command.split(" ")[1]
                    self.writen_format(full_command, self.writeGoTo(label))

                elif type_of_command == "CMD_IFGOTO":
                    label = full_command.split(" ")[1]
                    self.writen_format(full_command, self.writeIf(label))

                elif type_of_command == "CMD_FUNCTION":
                    functionName, nArgs = full_command.split(" ")[1:3]
                    self.writen_format(full_command, self.writeFunction(functionName, nArgs))

                elif type_of_command == "CMD_CALL":
                    functionName, nArgs = full_command.split(" ")[1:3]
                    self.writen_format(full_command, self.writeCall(functionName, nArgs))

                elif type_of_command in ["CMD_COMMENTS", "CMD_BREAKLINE"]:
                    continue

    def writeArithmetic(self, cmd_arithmetic):
        if cmd_arithmetic == "add":
            return ["@SP",'M=M-1', 'A=M', 'D=M', 'A=A-1','M=D+M'] 
        elif cmd_arithmetic == "sub":
            return ['@SP', 'M=M-1', 'A=M', 'D=M', 'A=A-1','M=M-D'] 
        elif cmd_arithmetic == "neg":
            return ['@SP', "M=M-1", 'A=M', 'M=-M', '@SP','M=M+1'] 
        elif cmd_arithmetic == "and":
            return ['@SP', 'M=M-1', 'A=M', 'D=M', 'A=A-1', 'M=D&M'] 
        elif cmd_arithmetic == "or": 
            return ['@SP', 'M=M-1', 'A=M', 'D=M', 'A=A-1', 'M=D|M'] 
        elif cmd_arithmetic == "not":
            return ['@SP', 'M=M-1', 'A=M', 'M=!M', '@SP', 'M=M+1'] 
        elif cmd_arithmetic == "eq":
            self.label += 1
            return ['@SP', "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", f"@eqTrue{self.label}", "D;JEQ", "@SP", "A=M-1", "M=0", f"(eqTrue{self.label})"]
        elif cmd_arithmetic =='gt': 
            self.label += 1
            return ['@SP', "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", f"@gtTrue{self.label}", "D;JGT", "@SP", "A=M-1", "M=0", f"(gtTrue{self.label})"]
        elif cmd_arithmetic =='lt': 
            self.label += 1
            return ['@SP', "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", f"@ltTrue{self.label}", "D;JLT", "@SP", "A=M-1", "M=0", f"(ltTrue{self.label})"]
        else:
            raise ValueError("Arithmetic or logic command error ") 

    def writePushPop(self, action, segment, index):   
        if action == "pop":
            if segment == "local":
                return ['@SP', 'M=M-1', '@LCL', 'D=M', f'@{index}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D'] 
            elif segment == "argument":
                return ['@SP', 'M=M-1', '@ARG', 'D=M', f'@{index}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D'] 
            elif segment == "this":
                return ['@SP', 'M=M-1', '@THIS', 'D=M', f'@{index}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D'] 
            elif segment == "that":
                return ['@SP', 'M=M-1', '@THAT', 'D=M', f'@{index}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D'] 
            elif segment == "constant":
                raise ValueError("You cant pop constants. Change your vm code.") 
            elif segment == "static":
                return ['@SP', 'M=M-1', 'A=M','D=M', f'@{self.file_title}.{index}', 'M=D'] 
            elif segment == "temp":
                return ['@SP', 'M=M-1', '@R5', 'D=A', f'@{index}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M','@R13', 'A=M', 'M=D'] 
            elif segment == "pointer":
                return ['@SP','M=M-1', '@R3', 'D=A', f'@{index}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D'] 
        elif action == "push":
            if segment == "local":
                return ['@LCL', 'D=M', f'@{index}', 'D=D+A', 'A=D', 'D=M','@SP','A=M', 'M=D', '@SP', 'M=M+1'] 
            elif segment == "argument":
                return ['@ARG', 'D=M', f'@{index}', 'D=D+A', 'A=D', 'D=M','@SP','A=M', 'M=D','@SP', 'M=M+1'] 
            elif segment == "this":
                return ['@THIS', 'D=M', f'@{index}', 'D=D+A', 'A=D', 'D=M','@SP','A=M', 'M=D', '@SP', 'M=M+1'] 
            elif segment == "that":
                return ['@THAT', 'D=M', f'@{index}', 'D=D+A', 'A=D', 'D=M','@SP','A=M', 'M=D', '@SP', 'M=M+1'] 
            elif segment == "constant":
                return [f'@{index}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] 
            elif segment == "static":
                return [f'@{self.file_title}.{index}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] 
            elif segment == "temp":
                return ['@R5', 'D=A', f'@{index}', 'D=D+A', 'A=D', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] 
            elif segment == "pointer":
                return ['@R3', 'D=A', f'@{index}', 'D=D+A', 'A=D', 'D=M', '@SP', 'A=M', 'M=D', '@SP','M=M+1'] 
            
    def writeLabel(self, label):
        return [f"({label})"]

    def writeGoTo(self, label):
        return [f"@{label}", "0,JMP"]

    def writeIf(self, label):
        return [f'@SP', 'M=M-1', 'A=M', 'D=M', f'@{label}', 'D;JNE']

    def writeFunction(self, functionName, nArgs):
        label = [f"({functionName})"]

    def writeCall(self, functionName, nArgs):
        returnAddress = [f"@returnAddress", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"] #!CHEQUEAR
        pushLcl= ["@LCL", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        pushArg= ["@ARG", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        pushThis= ["@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        pushThat= ["@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        repositionArg = ["@SP", "A=M", "D=M", f"@{nArgs}", "D=D-A", "@5", "D=D-A", "@ARG", "M=D"]
        repositionLcl = ["@SP", "D=M", "@LCL", "M=D"]
        jumpToCalledFunction = [f"@{functionName}", "0;JMP"]
        addressLabel = ["(returnAddress)"] #!CHEQUEAR
        return returnAddress + pushLcl + pushArg + pushThis + pushThat + repositionArg + repositionLcl + jumpToCalledFunction + addressLabel

    def writeReturn(self):
        pass

    def close(self):
        with open(f"{self.output_file}.asm", 'r') as file:
            file.close()