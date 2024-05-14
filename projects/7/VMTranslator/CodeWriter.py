#! CLASS WRITER  
class CodeWriter:
    def __init__(self, file_title):
        self.file_title = file_title
        self._eq_number = 0
        self._gt_number = 0
        self._lt_number = 0

    def clear(self):
        with open(f"{self.file_title}.asm", 'w'):
            pass

    def writen_format(self, command_description, asm_commands):
        with open(f"{self.file_title}.asm", "a") as asm_file:
            asm_file.write(f"// {command_description}\n")
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
                    action, segment, index = full_command.split(" ")[0:]
                    self.writen_format(full_command, self.writePushPop(action, segment, index))

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
            self._eq_number += 1
            return ['@SP', "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", f"@eqTrue{self._eq_number}", "D;JEQ", "@SP", "A=M-1", "M=0", f"(eqTrue{self._eq_number})"]
        elif cmd_arithmetic =='gt': 
            self._gt_number += 1
            return ['@SP', "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", f"@gtTrue{self._gt_number}", "D;JGT", "@SP", "A=M-1", "M=0", f"(gtTrue{self._gt_number})"]
        elif cmd_arithmetic =='lt': 
            self._lt_number += 1
            return ['@SP', "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", f"@ltTrue{self._lt_number}", "D;JLT", "@SP", "A=M-1", "M=0", f"(ltTrue{self._lt_number})"]
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

    def close(self):
        with open(f"{self.file_title}.asm", 'r') as file:
            file.close()