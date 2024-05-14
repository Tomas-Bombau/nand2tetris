#! CLASS WRITER
import os  
class CodeWriter:
    def __init__(self, output_file):
        self.output_file = output_file
        self.file_title = os.path.basename(output_file).split(".")[0]
        self.label = 0
        self.retFunction = 0

    def clear(self):
        with open(f"{self.output_file}.asm", 'w'):
            pass

    def writen_format(self, full_command, asm_commands):
        with open(f"{self.output_file}.asm", "a") as asm_file:
            asm_file.write(f"// {full_command}\n")
            for asm_code in asm_commands:
                    asm_file.write(f"{asm_code}\n")

    def write_file(self, parsed_commands):
        for commands in parsed_commands:
            for type_of_command, full_command in commands.items():
                parts = full_command.split(" ")
                action = parts[0]
                segment = parts[1] if len(parts) > 1 else None
                index = parts[2] if len(parts) > 2 else None

                if type_of_command == "CMD_ARITHMETIC":
                    self.writen_format(full_command, self.writeArithmetic(action))

                elif type_of_command in ["CMD_PUSH", "CMD_POP"]:
                    self.writen_format(full_command, self.writePushPop(action, segment, index))

                elif type_of_command == "CMD_LABEL":
                    self.writen_format(full_command, self.writeLabel(segment))

                elif type_of_command == "CMD_GOTO":
                    self.writen_format(full_command, self.writeGoTo(segment))

                elif type_of_command == "CMD_IFGOTO":
                    self.writen_format(full_command, self.writeIf(segment))

                elif type_of_command == "CMD_FUNCTION":
                    self.writen_format(full_command, self.writeFunction(segment, index))

                elif type_of_command == "CMD_CALL":
                    self.writen_format(full_command, self.writeCall(segment, index))

                elif type_of_command == "CMD_RETURN":
                    self.writen_format(full_command, self.writeReturn())

                elif type_of_command in ["CMD_COMMENTS", "CMD_BREAKLINE"]:
                    continue

    def writeArithmetic(self, action):
        if action == "add":
            return ["@SP",'M=M-1', 'A=M', 'D=M', 'A=A-1','M=D+M'] 
        elif action == "sub":
            return ['@SP', 'M=M-1', 'A=M', 'D=M', 'A=A-1','M=M-D'] 
        elif action == "neg":
            return ['@SP', "M=M-1", 'A=M', 'M=-M', '@SP','M=M+1'] 
        elif action == "and":
            return ['@SP', 'M=M-1', 'A=M', 'D=M', 'A=A-1', 'M=D&M'] 
        elif action == "or": 
            return ['@SP', 'M=M-1', 'A=M', 'D=M', 'A=A-1', 'M=D|M'] 
        elif action == "not":
            return ['@SP', 'M=M-1', 'A=M', 'M=!M', '@SP', 'M=M+1'] 
        elif action == "eq":
            self.label += 1
            return ['@SP', "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", f"@eqTrue{self.label}", "D;JEQ", "@SP", "A=M-1", "M=0", f"(eqTrue{self.label})"]
        elif action =='gt': 
            self.label += 1
            return ['@SP', "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", f"@gtTrue{self.label}", "D;JGT", "@SP", "A=M-1", "M=0", f"(gtTrue{self.label})"]
        elif action =='lt': 
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
            
    def writeLabel(self, segment):
        return [f"({segment})"]

    def writeGoTo(self, segment):
        return [f"@{segment}", "0,JMP"]

    def writeIf(self, segment):
        return [f'@SP', 'M=M-1', 'A=M', 'D=M', f'@{segment}', 'D;JNE']

    def writeFunction(self, functionName, nVars):
        label = [f'({functionName})']
        limits = ['@i', 'M=0', f'@{nVars}', 'D=A', '@numberVars', 'M=D']
        condition = [f'({functionName}$LOOP)', '@numberVars', 'D=M', '@i', 'D=D-M', f'@{functionName}$ENDLOOP', 'D;JEQ']
        pushVars = ['@SP', 'A=M', 'M=0']
        addOneToI = ['@i', 'M=M+1']
        moveSP = ['@SP', 'M=M+1']
        backToCondition = [f'@{functionName}$LOOP', '0,JMP']
        endLabel = [f'({functionName}$ENDLOOP)']
        return label + limits + condition + pushVars + moveSP + addOneToI + backToCondition + endLabel 

    def writeCall(self, functionName, nArgs):
        returnAddress = [f"@{functionName}$ret.{self.retFunction}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        pushLcl= ["@LCL", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        pushArg= ["@ARG", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        pushThis= ["@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        pushThat= ["@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        repositionArg = ["@SP", "D=M", f"@{nArgs}", "D=D-A", "@5", "D=D-A", "@ARG", "M=D"]   
        repositionLcl = ["@SP", "D=M", "@LCL", "M=D"]
        jumpToCalledFunction = [f"@{functionName}", "0;JMP"]
        addressLabel = [f"({functionName}$ret.{self.retFunction})"] 
        self.retFunction += 1
        return returnAddress + pushLcl + pushArg + pushThis + pushThat + repositionArg + repositionLcl + jumpToCalledFunction + addressLabel

    def writeReturn(self):
        endFrame = ['@LCL', 'D=M', '@endFrame', 'M=D']
        retAddr = ['@endFrame', 'D=M', '@5', 'A=D-A', 'D=M', '@retAddr', 'M=D']
        retValue = ['@SP', 'M=M-1', 'A=M', 'D=M', '@ARG', 'A=M', 'M=D']
        restoreSP = ['@ARG', 'M=M+1', 'D=M', '@SP', 'M=D'] 
        restoreThat = ['@endFrame', 'M=M-1', 'A=M', 'D=M', '@THAT', 'M=D'] 
        restoreThis = ['@endFrame', 'M=M-1', 'A=M', 'D=M', '@THIS', 'M=D']
        restoreArg = ['@endFrame', 'M=M-1', 'A=M', 'D=M', '@ARG', 'M=D']
        restoreLcl = ['@endFrame', 'M=M-1', 'A=M', 'D=M', '@LCL', 'M=D']
        returnToRetAddr = ['@retAddr', 'A=M', '0;JMP']
        return endFrame + retAddr + retValue + restoreSP + restoreThat + restoreThis + restoreArg + restoreLcl + returnToRetAddr

    def close(self):
        with open(f"{self.output_file}.asm", 'r') as file:
            file.close()