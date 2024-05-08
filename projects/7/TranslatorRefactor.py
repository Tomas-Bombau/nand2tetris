import os

# #! CLASS PARSER
class Parser:
    def __init__(self, filename):
        self.all_lines = []
        self.filename = filename
        self.file_title = ""

    def read_vm_file(self, filename):
        with open(filename) as vm_code:
            for line in vm_code:
                self.all_lines.append(line.strip())
        return self.all_lines
    
    def title(self):
        self.file_title = self.filename.split("/")[-1].split(".")[0]
        return self.file_title

    def command_type(self, commands):
            if commands.startswith("/"):
                return "CMD_COMMENTS"
            elif commands == "":
                return "CMD_BREAKLINE"
            elif "push" in commands:
                return "CMD_PUSH"
            elif "pop" in commands:
                return "CMD_POP"
            elif "add" or "sub" or 'neg' or 'eq' or 'gt' or 'lt' or 'and' or 'or' or 'not' in commands:
                return "CMD_ARITHMETIC"
        
#! CLASS WRITER  
class WriterCode:
    def __init__(self, file_title):
        self.file_title = file_title
        self.label = 0

    def clear(self):
        with open(f"{self.file_title}.asm", 'w'):
            pass

    def process_commands(self, file_commands, parser):
        for command in file_commands:
            type_of_command = parser.command_type(command)

            if type_of_command == "CMD_ARITHMETIC":
                arithmetic_asm = self.arithmetic_to_asm(command)
                self.write(command, arithmetic_asm)

            elif type_of_command in ["CMD_PUSH", "CMD_POP"]:
                action, segment, index = command.split(" ")[0:]
                segments_asm = self.pop_push_segments_to_asm(action, segment, index)
                self.write(command, segments_asm)

            elif type_of_command in ["CMD_COMMENTS", "CMD_BREAKLINE"]:
                continue

    def write(self, command_description, asm_commands):
        with open(f"{self.file_title}.asm", "a") as asm_file:
            asm_file.write(f"// {command_description}\n")
            for asm_code in asm_commands:
                    asm_file.write(f"{asm_code}\n")

    def arithmetic_to_asm(self, cmd_arithmetic):
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

    def pop_push_segments_to_asm(self, action, segment, index):   
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
            

def main(path):
    file = Parser(path)
    file_title = file.title()
    file_commands = file.read_vm_file(path)
    asm_code = WriterCode(file_title)
    asm_code.clear()
    asm_code.process_commands(file_commands, file)


path = './projects/7/StackArithmetic/StackTest/StackTest.vm'
main(path)
