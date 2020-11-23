from interpreter.directions import Direction, CC


class BaseCommand:
    def __init__(self, stack: []):
        self.stack = stack
        self.name = 'no_action'
        self.description = 'this command does nothing'
        self.arguments = None

    def __call__(self):
        self.execute()

    def execute(self):
        return

    def __repr__(self):
        return (f'name: {self.name}, description: '
                f'{self.description}, args: {self.arguments}')


class Push(BaseCommand):
    def __init__(self, stack: [], value: int):
        super().__init__(stack)
        self.name = 'push'
        self.description = 'pushes the number of previous color block\'s' \
                           ' pixels on the stack'
        self.arguments = value

    def execute(self):
        self.stack.append(self.arguments)


class Pop(BaseCommand):
    def __init__(self, stack: []):
        super().__init__(stack)
        self.name = 'pop'
        self.description = 'pops the top value of stack'

    def execute(self):
        if len(self.stack) == 0:
            return
        self.arguments = self.stack.pop()


class Calculate(BaseCommand):
    def __init__(self, stack: [], name: str,
                 calculate_func: callable, index: int):
        super().__init__(stack)
        self.name = name
        self.calculate_func = calculate_func
        self.index = index
        self.description = self.set_description()

    def set_description(self):
        start = 'pops two stack\'s values, '
        end = ', pushes the result on the stack'
        if self.calculate_func == int.__sub__:
            return f'{start}subtracts the top value from ' \
                   f'the previous one{end}'
        if self.calculate_func == int.__add__:
            return f'{start}adds them{end}'
        if self.calculate_func == int.__mul__:
            return f'{start}multiplies them{end}'
        if self.index == 0:
            return f'{start}calculates the integer part of dividing ' \
                   f'the top by the previous{end}'
        return f'{start}calculates the remainder of dividing the top ' \
               f'by the previous{end}'

    def execute(self):
        if len(self.stack) < 2:
            return
        a = self.stack.pop()
        b = self.stack.pop()
        self.arguments = (b, a)
        if self.index != -1:
            a = abs(a) if self.index == 1 else a
            self.stack.append(self.calculate_func(b, a)[self.index])
            return
        self.stack.append(self.calculate_func(b, a))


class Not(BaseCommand):
    def __init__(self, stack: []):
        super().__init__(stack)
        self.name = 'not'
        self.description = 'replaces the top value of the stack with 0 if ' \
                           'the top value is 1, else with 1'

    def execute(self):
        if len(self.stack) == 0:
            return
        old_value = self.stack.pop()
        self.arguments = old_value
        self.stack.append(1 if old_value == 0 else 0)


class Greater(BaseCommand):
    def __init__(self, stack: []):
        super().__init__(stack)
        self.name = 'greater'
        self.description = 'pops two values of the stack, pushes 1 if ' \
                           'previous is greater then top, else 0'

    def execute(self):
        if len(self.stack) < 2:
            return
        a = self.stack.pop()
        b = self.stack.pop()
        self.arguments = (b, a)
        self.stack.append(1 if b > a else 0)


class Pointer(BaseCommand):
    def __init__(self, stack: [], dp: Direction):
        super().__init__(stack)
        self.name = 'pointer'
        self.description = 'pops the value from stack, rotate dp ' \
                           'clockwise absolute of this value if ' \
                           'value > 0, else rotate counterclockwise)'
        self.dp = dp

    def execute(self):
        if len(self.stack) != 0:
            turn_count = self.stack.pop()
            self.arguments = turn_count
            for i in range(abs(turn_count)):
                self.dp = self.dp.next(turn_count > 0)


class Switch(BaseCommand):
    def __init__(self, stack: [], cc: CC):
        super().__init__(stack)
        self.name = 'switch'
        self.description = 'pops the value from stack, rotate cc absolute of value times'
        self.cc = cc

    def execute(self):
        if len(self.stack) != 0:
            turn_count = self.stack.pop()
            self.arguments = turn_count
            for i in range(abs(turn_count)):
                self.cc = self.cc.next()


class Duplicate(BaseCommand):
    def __init__(self, stack: []):
        super().__init__(stack)
        self.name = 'duplicate'
        self.description = ''

    def execute(self):
        if len(self.stack) == 0:
            return
        self.arguments = self.stack[-1]
        self.stack.append(self.stack[-1])


class Roll(BaseCommand):
    def __init__(self, stack: []):
        super().__init__(stack)
        self.name = 'roll'
        self.description = ''

    # берем depth последних элементов листа и прокручиваем их
    # с шагом count, -count - влево, +count - вправо
    def execute(self):
        if len(self.stack) < 2 or self.stack[-2] < 0:
            return
        count = self.stack.pop()
        depth = self.stack.pop()
        self.arguments = (depth, count)
        if depth == 1:
            return
        count %= depth
        index = -abs(count) + depth * (count < 0)
        self.stack[-depth:] = self.stack[index:] + self.stack[-depth:index]


class InInt(BaseCommand):
    def __init__(self, stack: []):
        super().__init__(stack)
        self.name = 'in_int'
        self.description = ''

    def execute(self):
        input_value = input()
        try:
            self.stack.append(int(input_value))
            self.arguments = input_value
        except ValueError:
            return


class InChar(BaseCommand):
    def __init__(self, stack):
        super().__init__(stack)
        self.name = 'in_char'
        self.description = ''

    def execute(self):
        input_value = input()
        try:
            if len(input_value) > 1:
                return
            self.stack.append(ord(input_value))
            self.arguments = input_value
        except TypeError:
            return
        except ValueError:
            return


class OutInt(BaseCommand):
    def __init__(self, stack: []):
        super().__init__(stack)
        self.name = 'out_int'
        self.description = ''

    def execute(self):
        if len(self.stack) == 0:
            return
        out_value = self.stack.pop()
        self.arguments = out_value
        print(out_value, end='')


class OutChar(BaseCommand):
    def __init__(self, stack: []):
        super().__init__(stack)
        self.name = 'out_char'
        self.description = ''

    def execute(self):
        if len(self.stack) == 0:
            return
        try:
            out_value = self.stack.pop()
            print(chr(out_value), end='')
            self.arguments = out_value
        except ValueError:
            return
