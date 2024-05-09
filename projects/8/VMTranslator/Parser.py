
# #! CLASS PARSER
class Parser:
    def __init__(self, filename):
        self.all_lines = []
        self.filename = filename
        self.file_title = filename.split("/")[-1].split(".")[0]

    def title(self):
        return self.file_title

    def read_vm_file(self):
        with open(self.filename, "r") as vm_code:
            for line in vm_code:
                self.all_lines.append(line.strip())
        return self.all_lines
    
    def command_type(self, commands):
            if commands.startswith("/"):
                return "CMD_COMMENTS"
            elif commands == "":
                return "CMD_BREAKLINE"
            elif "push" in commands:
                return "CMD_PUSH"
            elif "pop" in commands:
                return "CMD_POP"
            elif any(op in commands for op in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']):
                return "CMD_ARITHMETIC"
            elif "label" in commands:
                return "CMD_LABEL"
            elif "if-goto" in commands:
                return "CMD_IFGOTO"
            elif "goto" in commands:
                return "CMD_GOTO"
            
    def process_commands(self):
        self.commands = []
        for command in self.all_lines:
            type_of_command = self.command_type(command)
            command = command.split("//")[0].strip()
            self.commands.append({type_of_command: command})
        return self.commands