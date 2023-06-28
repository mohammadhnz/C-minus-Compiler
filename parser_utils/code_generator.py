class SymbolTable:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def pop_entry(self):
        return self.entries.pop()

    def get_address(self, identifier):
        for entry in reversed(self.entries):
            if entry[0] == identifier:
                return entry[2]
        return None

    def get_address_type(self, address):
        for entry in reversed(self.entries):
            if entry[2] == address:
                return entry[1]
        return None

    def collapse_table(self, to_keep):
        self.entries = self.entries[:to_keep]


def log_codes():
    with open("output.txt", 'w') as file:
        for inst in enumerate(code_generator.program_block.code_memory):
            file.write(f'{inst[0]}\t{inst[1]}\n')
    with open('semantic_errors.txt', 'w') as file:
        if not code_generator.errors:
            file.write('The input program is semantically correct.')
        else:
            for error in code_generator.errors:
                file.write(error + "\n")


class Memory:
    def __init__(self) -> None:
        self.data_address, self.temp_address = 100, 500

    def get_temp_address(self):
        self.temp_address += 4
        return self.temp_address - 4

    def get_data_address(self):
        self.data_address += 4
        return self.data_address - 4


class ProgramBlock:
    def __init__(self):
        self.code_memory = []
        self.index = 0

    def add_instruction(self, index, operator, arg1, arg2='', arg3=''):
        self._fill_memory(index)
        self.code_memory[index] = f'({operator}, {arg1}, {arg2}, {arg3})'

    def _fill_memory(self, index):
        while len(self.code_memory) <= index:
            self.code_memory.append('')

    def initialize_variables(self, memory, symbol_table, lexeme):
        symbol_table.add_entry((lexeme, 'int', str(memory.get_data_address())))

    def initialize_array(self, memory, symbol_table, lexeme, length):
        data_addresses = [str(memory.get_data_address()) for _ in range(length + 1)]
        self.add_instruction(self.index, 'ASSIGN', f'#{data_addresses[1]}', data_addresses[0])
        self.index += 1
        symbol_table.add_entry((lexeme, 'array', data_addresses[0]))

    def forward(self):
        self.index += 1


class CodeGenerator:
    def __init__(self):
        self.program_block = ProgramBlock()
        self.memory = Memory()
        self.symbol_table = SymbolTable()
        self.semantic_stack = []
        self.scope_stack = []
        self.break_stack = []
        self.errors = []

    def get_semantic_stack_last(self):
        return len(self.semantic_stack) - 1

    def code_gen(self, token, action):
        return getattr(self, action)(token)

    def semantic_check(self, token, action):
        return getattr(self, action)(token)

    def pid(self, identifier):
        if identifier == 'output':
            return self.semantic_stack.append('output')
        self.semantic_stack.append(self.symbol_table.get_address(identifier))

    def pnum(self, num):
        self.semantic_stack.append('#' + num)

    def start(self, *args):
        self.scope_stack.append(len(self.symbol_table.entries))

    def end(self, *args):
        self.symbol_table.collapse_table(self.scope_stack.pop())

    def push_lexeme(self, lexeme):
        self.semantic_stack.append(lexeme)

    def set_variable(self, *args):
        self.program_block.initialize_variables(self.memory, self.symbol_table, self.semantic_stack.pop())

    def set_array(self, *args):
        length, lexeme = int(self.semantic_stack.pop()[1:]), self.semantic_stack.pop()
        self.program_block.initialize_array(self.memory, self.symbol_table, lexeme, length)

    def label(self, *args):
        self.semantic_stack.append(self.program_block.index)

    def until(self, *args):
        self.program_block.add_instruction(
            self.program_block.index,
            'JPF',
            self.semantic_stack.pop(),
            self.semantic_stack.pop(),
            ''
        )
        self.program_block.forward()

    def start_break(self, *args):
        self.break_stack.append('BREAK_CP')

    def break_func(self, *args):
        self.break_stack.append(self.program_block.index)
        self.program_block.forward()

    def end_break(self, *args):
        for i in reversed(self.break_stack):
            if i == 'BREAK_CP':
                self.break_stack.pop()
                break
            self.break_stack.pop()
            self.program_block.add_instruction(i, 'JP', str(self.program_block.index), '', '')

    def get_temp(self, *args):
        temp_address = self.memory.get_temp_address()
        self.semantic_stack.append(temp_address)
        self.program_block.add_instruction(self.program_block.index, 'ASSIGN', '#0', str(temp_address))
        self.program_block.forward()

    def pop(self, *args):
        self.semantic_stack.pop()

    def save(self, *args):
        self.semantic_stack.append(self.program_block.index)
        self.program_block.forward()

    def save_jpf(self, *args):
        current_index = self.program_block.index
        top_of_stack = self.semantic_stack.pop()
        after_else_index = self.semantic_stack.pop()

        target_index = current_index + 1
        self.program_block.add_instruction(int(top_of_stack), 'JPF', after_else_index, str(target_index))
        self.semantic_stack.append(current_index)
        self.program_block.forward()

    def jump(self, *args):
        after_else = self.semantic_stack.pop()
        self.program_block.add_instruction(int(after_else), 'JP', str(self.program_block.index))

    def assign_value(self, *args):
        value = self.semantic_stack.pop()
        assignee = self.semantic_stack[self.get_semantic_stack_last()]
        current_index = self.program_block.index
        self.program_block.add_instruction(current_index, 'ASSIGN', value, assignee)
        self.program_block.forward()

    def perform_operation(self, *args):
        temporary_address = self.memory.get_temp_address()
        current_index = self.program_block.index
        second_operand = self.semantic_stack.pop()
        operator = self.semantic_stack.pop()
        first_operand = self.semantic_stack.pop()
        operators = {'+': 'ADD', '-': 'SUB', '==': 'EQ', '<': 'LT'}
        self.program_block.add_instruction(current_index, operators[operator], first_operand, second_operand,
                                           temporary_address)
        self.semantic_stack.append(temporary_address)
        self.program_block.forward()

    def multiply(self, *args):
        temporary_address = self.memory.get_temp_address()
        current_index = self.program_block.index
        first_operand = self.semantic_stack.pop()
        second_operand = self.semantic_stack.pop()

        self.program_block.add_instruction(current_index, 'MULT', first_operand, second_operand, temporary_address)
        self.program_block.forward()
        self.semantic_stack.append(temporary_address)

    def output_value(self, *args):
        output_name = self.semantic_stack[self.get_semantic_stack_last() - 1]

        if output_name == 'output':
            value_to_print = self.semantic_stack.pop()
            self.program_block.add_instruction(self.program_block.index, 'PRINT', value_to_print)
            self.program_block.forward()

    def assign_array_index(self, *args):
        index = self.semantic_stack.pop()
        address = self.semantic_stack.pop()

        multiplied_index = str(self.memory.get_temp_address())
        self.program_block.add_instruction(self.program_block.index, 'MULT', '#4', index, multiplied_index)
        self.program_block.forward()

        address_copy = str(self.memory.get_temp_address())
        self.program_block.add_instruction(self.program_block.index, 'ASSIGN', address, address_copy)
        self.program_block.forward()

        calculated_index = str(self.memory.get_temp_address())
        self.program_block.add_instruction(self.program_block.index, 'ADD', address_copy, multiplied_index,
                                           calculated_index)
        self.program_block.forward()

        self.semantic_stack.append('@' + calculated_index)

    ## Semantic Checks
    def declaration_check(self, token):
        if token[1] == 'output':
            return True
        if self.symbol_table.get_address(token[1]) is None:
            if token[1] not in self.semantic_stack:
                self.errors.append(f"#{token[2]}: Semantic Error! '{token[1]}' is not defined.")
                return False
        return True

    def check_void_id(self, token):
        if token[1] != '(':
            a = self.semantic_stack.pop()
            self.errors.append(f"#{token[2]}: Semantic Error! Illegal type of void for '{a}'.")
            return False
        return True

    def check_break(self, token):
        if not self.break_stack:
            self.errors.append(f"#{token[2]}: Semantic Error! No 'repeat ... until' found for 'break'.")
            return False, False
        return True

    def check_operation(self, token):
        second_operand = self.semantic_stack.pop()
        operator = self.semantic_stack.pop()
        first_operand = self.semantic_stack.pop()
        response = True
        a = self.symbol_table.get_address_type(first_operand)
        b = self.symbol_table.get_address_type(second_operand)
        if a != b:
            if 'array' in [a, b]:
                self.errors.append(
                    f"#{token[2]}: Semantic Error! Type mismatch in operands, Got array instead of int."
                )
                response = False, True
        self.semantic_stack.append(first_operand)
        self.semantic_stack.append(operator)
        self.semantic_stack.append(second_operand)
        return response


code_generator = CodeGenerator()


def code_gen(token, action):
    code_generator.code_gen(token, action)


def semantic_check(token, action):
    return code_generator.semantic_check(token, action)
