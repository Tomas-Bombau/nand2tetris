# #! CLASS PARSER
import os

class Parser:
    def __init__(self, input_file):
        self.all_lines = []
        self.input_file = input_file
        self.filename = os.path.basename(input_file).split(".")[0]

    def title(self):
        return self.filename

    def read_vm_file(self):
        with open(self.input_file, "r") as vm_code:
            for line in vm_code:
                self.all_lines.append(line.strip())
        return self.all_lines
    
    def command_type(self, commands):
            command = commands.split("//")[0].strip() 
            if command.startswith("/"):
                return "CMD_COMMENTS"
            elif command == "":
                return "CMD_BREAKLINE"
            elif command == 'add':
                return "CMD_ARITHMETIC"
            elif command == 'sub':
                return "CMD_ARITHMETIC"
            elif command == 'neg':
                return "CMD_ARITHMETIC"
            elif command == 'gt':
                return "CMD_ARITHMETIC"
            elif command == 'lt':
                return "CMD_ARITHMETIC"
            elif command == 'and':
                return "CMD_ARITHMETIC"
            elif command == 'or':
                return "CMD_ARITHMETIC"
            elif command == 'not':
                return "CMD_ARITHMETIC"
            elif "label" in command:
                return "CMD_LABEL"
            elif "if-goto" in command:
                return "CMD_IFGOTO"
            elif "goto" in command:
                return "CMD_GOTO"
            elif "function" in command:
                return "CMD_FUNCTION"
            elif "call" in command:
                return "CMD_CALL"
            elif "return" in command:
                return "CMD_RETURN"
            elif "push" in command:
                return "CMD_PUSH"
            elif "pop" in commands:
                return "CMD_POP"

            
    def process_commands(self):
        self.commands = []
        self.read_vm_file()
        for command in self.all_lines:
            type_of_command = self.command_type(command)
            self.commands.append({type_of_command: command})
        return self.commands