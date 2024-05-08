#Function to read VM file
def read_vm_file(filename):
    all_lines = []
    with open(filename) as vm_code:
        for line in vm_code:
            all_lines.append(line.strip())
    return all_lines

#Function to write ASM file
def write_asm_file(title, command, asm_commands):
    with open(f"{title}.asm", "a") as asm_file:
        asm_file.write(f"// {command}\n")
        for asm_line in asm_commands:
                asm_file.write(f"{asm_line}\n")

#Function to know COMMAND applied:
def commandType(commands):
        if "return" in commands:
            return "CMD_RETURN"
        elif commands.startswith("/"):
            return "CMD_COMMENTS"
        elif commands == "":
            return "CMD_BREAKLINE"
        elif "push" in commands:
            return "CMD_PUSH"
        elif "pop" in commands:
            return "CMD_POP"
        elif "add" or "sub" or 'neg' or 'eq' or 'gt' or 'lt' or 'and' or 'or' or 'not' in commands:
            return "CMD_ARITHMETIC"
        
        
#Function of ARITHMETIC commands
label = 0
def arithmetic_to_asm(cmd_arithmetic):
    global label
    if cmd_arithmetic == "add":
        return ["@SP",'M=M-1', 'A=M', 'D=M', 'A=A-1','M=D+M'] #!OK
    elif cmd_arithmetic == "sub":
        return ['@SP', 'M=M-1', 'A=M', 'D=M', 'A=A-1','M=M-D'] #!OK
    elif cmd_arithmetic == "neg":
        return ['@SP', "M=M-1", 'A=M', 'M=-M', '@SP','M=M+1'] #!OK
    elif cmd_arithmetic == "and":
        return ['@SP', 'M=M-1', 'A=M', 'D=M', 'A=A-1', 'M=D&M'] #!OK
    elif cmd_arithmetic == "or": 
        return ['@SP', 'M=M-1', 'A=M', 'D=M', 'A=A-1', 'M=D|M'] #!OK
    elif cmd_arithmetic == "not":
        return ['@SP', 'M=M-1', 'A=M', 'M=!M', '@SP', 'M=M+1'] #!OK
    elif cmd_arithmetic == "eq":
        label += 1
        return ['@SP', "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", f"@eqTrue{label}", "D;JEQ", "@SP", "A=M-1", "M=0", f"(eqTrue{label})"]
    elif cmd_arithmetic =='gt': 
        label += 1
        return ['@SP', "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", f"@gtTrue{label}", "D;JGT", "@SP", "A=M-1", "M=0", f"(gtTrue{label})"]
    elif cmd_arithmetic =='lt': 
        label += 1
        return ['@SP', "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", f"@ltTrue{label}", "D;JLT", "@SP", "A=M-1", "M=0", f"(ltTrue{label})"]
    else:
        raise ValueError("Arithmetic or logic command error ") #!OK
    
#Function of PUSH/SEGMENTS commands
def push_segments_to_asm(arg_action, arg_segment, arg_i, file_title):
        if arg_segment == "local":
            return ['@LCL', 'D=M', f'@{arg_i}', 'D=D+A', 'A=D', 'D=M','@SP','A=M', 'M=D', '@SP', 'M=M+1'] #!OK
        elif arg_segment == "argument":
            return ['@ARG', 'D=M', f'@{arg_i}', 'D=D+A', 'A=D', 'D=M','@SP','A=M', 'M=D','@SP', 'M=M+1'] #!OK
        elif arg_segment == "this":
            return ['@THIS', 'D=M', f'@{arg_i}', 'D=D+A', 'A=D', 'D=M','@SP','A=M', 'M=D', '@SP', 'M=M+1'] #!OK
        elif arg_segment == "that":
            return ['@THAT', 'D=M', f'@{arg_i}', 'D=D+A', 'A=D', 'D=M','@SP','A=M', 'M=D', '@SP', 'M=M+1'] #!OK
        elif arg_segment == "constant":
            return [f'@{arg_i}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] #!OK
        elif arg_segment == "static":
            return [f'@{file_title}.{arg_i}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] #!OK
        elif arg_segment == "temp":
            return ['@R5', 'D=A', f'@{arg_i}', 'D=D+A', 'A=D', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] #!OK
        elif arg_segment == "pointer":
            return ['@R3', 'D=A', f'@{arg_i}', 'D=D+A', 'A=D', 'D=M', '@SP', 'A=M', 'M=D', '@SP','M=M+1'] #!OK

#Function of POP/SEGMENTS commands
def pop_segments_to_asm(arg_action, arg_segment, arg_i, file_title):   
        if arg_segment == "local":
            return ['@SP', 'M=M-1', '@LCL', 'D=M', f'@{arg_i}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D'] #!OK
        elif arg_segment == "argument":
            return ['@SP', 'M=M-1', '@ARG', 'D=M', f'@{arg_i}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D'] #!OK
        elif arg_segment == "this":
            return ['@SP', 'M=M-1', '@THIS', 'D=M', f'@{arg_i}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D'] #!OK
        elif arg_segment == "that":
            return ['@SP', 'M=M-1', '@THAT', 'D=M', f'@{arg_i}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D'] #!OK
        elif arg_segment == "constant":
            raise ValueError("You cant pop constants. Change your vm code.") #!OK
        elif arg_segment == "static":
            return ['@SP', 'M=M-1', 'A=M','D=M', f'@{file_title}.{arg_i}', 'M=D'] #!OK
        elif arg_segment == "temp":
            return ['@SP', 'M=M-1', '@R5', 'D=A', f'@{arg_i}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M','@R13', 'A=M', 'M=D'] #!OK
        elif arg_segment == "pointer":
            return ['@SP','M=M-1', '@R3', 'D=A', f'@{arg_i}', 'D=D+A', '@R13', 'M=D', '@SP', 'A=M', 'D=M', '@R13', 'A=M', 'M=D'] #!OK

def main(vm_file):
    #File Title
    file_title = vm_file.split("/")[-1].split(".")[0]
    #Everytime we execute the translator, the file's data gets erase
    with open(f"{file_title}.asm", 'w'):
        pass
    #Reading File
    list_command_lines = read_vm_file(vm_file)
    #Analyzing each command
    for command in list_command_lines:
        type_of_command = commandType(command)
        if type_of_command == "CMD_ARITHMETIC":
            write_asm_file(file_title, command, arithmetic_to_asm(command))

        elif type_of_command == "CMD_PUSH":
            commands_args = command.split(" ")
            arg_action = commands_args[0]
            arg_segment = commands_args[1]
            arg_i = commands_args[2]
            write_asm_file(file_title, command, push_segments_to_asm(arg_action, arg_segment, arg_i, file_title))

        elif type_of_command == "CMD_POP":
            commands_args = command.split(" ")
            arg_action = commands_args[0]
            arg_segment = commands_args[1]
            arg_i = commands_args[2]
            write_asm_file(file_title, command, pop_segments_to_asm(arg_action, arg_segment, arg_i, file_title))

        elif type_of_command == "CMD_COMMENTS":
            continue

        elif type_of_command == "CMD_BREAKLINE":
            continue

        elif type_of_command == "CMD_RETURN":
            return

main("./StackArithmetic/StackTest/StackTest.vm")