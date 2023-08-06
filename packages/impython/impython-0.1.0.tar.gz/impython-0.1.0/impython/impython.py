class ImPython:
    def __init__(self) -> None:
        self.G = globals()
        self.L = self.G
        self.globals = {}
        self.locals = {}
        self.block = ''
        self.hint = ''
        self.running = True

    def get_block(self) -> str:
        block = self.block
        self.block = ''
        return block

    def set_command(self, command):
        self.block += command+'\n'

    def meta_command(self, command:str) -> bool:
        if command[0] == '$':
            if ':' in command:
                return command[1:].split(':', 1)
            else:
                return command[1:], ''
        else:
            return None

    def exec(self):
        exec(self.get_block(), self.G, self.L)

    def set_local(self, name):
        if name in self.locals:
            self.L = self.locals[name]
        else:
            self.L = {}
            self.locals[name] = self.L

    def set_global(self, name):
        if name in self.globals:
            self.G = self.globals[name]
        else:
            self.G = {}
            self.globals[name] = self.G

    def reset(self):
        self.G = globals()
        self.L = self.G

    def clear(self):
        self.block = ''

    def set_hint(self, hint):
        self.hint = hint

    def show_block(self):
        print(self.block)

    def show_local(self):
        print(self.L)

    def show_global(self):
        print(self.G)

    def exit(self):
        self.running = False

    def get_next_command(self):
        command = input(self.hint)
        meta = self.meta_command(command)
        if meta:
            self.execute_meta_command(meta)
        else:
            self.set_command(command)

    def execute_meta_command(self, meta):
        command, params = meta
        if command == 'exec':
            self.exec()
        elif command == 'local':
            self.set_local(params)
        elif command == 'global':
            self.set_global(params)
        elif command == 'reset':
            self.reset()
        elif command == 'clear':
            self.clear()
        elif command == 'show_block':
            self.show_block()
        elif command == 'show_local':
            self.show_local()
        elif command == 'show_global':
            self.show_global()
        elif command == 'exit':
            self.exit()
        elif command == 'hint':
            self.set_hint(params)
        else:
            raise Exception(f'no meta command called {command}')

    def run(self) -> None:
        while self.running:
            self.get_next_command()
