from interpreter.directions import Direction, CC


class BaseCommand:
    def __init__(self, stack: []):
        self.stack = stack
        self.name = 'no_action'
        self.description = 'эта команда ничего не делает'
        self.arguments = None

    def __call__(self):
        self.execute()

    def execute(self):
        return

    def __repr__(self):
        return (f'\tназвание: {self.name},\n\tописание: '
                f'{self.description},\n\tаргументы: {self.arguments}')


class Push(BaseCommand):
    def __init__(self, stack: [], value: int):
        super().__init__(stack)
        self.name = 'push'
        self.description = 'кладет в стэк число, ' \
                           'равное количеству пикселей в предыдущем блоке'
        self.arguments = value

    def execute(self):
        self.stack.append(self.arguments)


class Pop(BaseCommand):
    def __init__(self, stack: []):
        super().__init__(stack)
        self.name = 'pop'
        self.description = 'убирает верхнее значение стэка'

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
        start = 'убирает два значения стэка, '
        end = ', кладет результат обратно в стэк'
        if self.calculate_func == int.__sub__:
            return f'{start}вычитает верхнее значение из предыдущего{end}'
        if self.calculate_func == int.__add__:
            return f'{start}складывает их{end}'
        if self.calculate_func == int.__mul__:
            return f'{start}умножает их{end}'
        if self.index == 0:
            return f'{start}делит нацело предыдущее значение на верхнее{end}'
        return f'{start}вчисляет остаток от деления предыдущего ' \
               f'значения на верхнее{end}'

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
        self.description = 'заменяет верхнее значение стэка на 0,' \
                           ' если оно было равно 1, иначе на 1'

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
        self.description = 'убирает два значения из стэка, кладет в ' \
                           'него 1, если предыдущее значение было ' \
                           'больше верхнего, иначе кладет 0'

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
        self.description = 'убирает значение(далее х) из стэка, ' \
                           'меняет dp по часовой стрелке abs(x) раз, если' \
                           'х > 0, иначе - против часовой'
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
        self.description = 'убирает значение(далее х) из стэка, ' \
                           'меняет cc abs(x) раз'
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
        self.description = 'дублирует в стэк его верхнее значение'

    def execute(self):
        if len(self.stack) == 0:
            return
        self.arguments = self.stack[-1]
        self.stack.append(self.stack[-1])


class Roll(BaseCommand):
    def __init__(self, stack: []):
        super().__init__(stack)
        self.name = 'roll'
        self.description = 'убирает два значения из стэка, ' \
                           '\n\t\t верхнее - count, предыдущее - depth, ' \
                           '\n\t\t depth не может быть отрицательным, ' \
                           '\n\t\t берет depth последних элементов стэка и ' \
                           '\n\t\t циклически сдвигает их с шагом count ' \
                           '\n\t\t (count > 0 - вправо, count < 0 - влево)'

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
    def __init__(self, stack: [], step_by_step: bool):
        super().__init__(stack)
        self.step_by_step = step_by_step
        self.name = 'in_int'
        self.description = 'кладет введенное с консоли целое число в стэк'

    def execute(self):
        if self.step_by_step:
            input_value = input('ВВОД:')
        else:
            input_value = input()
        try:
            self.stack.append(int(input_value))
            self.arguments = input_value
        except ValueError:
            return


class InChar(BaseCommand):
    def __init__(self, stack: [], step_by_step: bool):
        super().__init__(stack)
        self.step_by_step = step_by_step
        self.name = 'in_char'
        self.description = 'кладет ord(введенный в консоль символ) в стэк'

    def execute(self):
        if self.step_by_step:
            input_value = input('ВВОД:')
        else:
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
    def __init__(self, stack: [], step_by_step=False):
        super().__init__(stack)
        self.step_by_step = step_by_step
        self.name = 'out_int'
        self.description = 'убирает значение из стэка и выводит его в консоль'

    def execute(self):
        if len(self.stack) == 0:
            return
        out_value = self.stack.pop()
        self.arguments = out_value
        if self.step_by_step:
            print(f'\nВЫВОД:{out_value}\n')
        else:
            print(out_value, end='')


class OutChar(BaseCommand):
    def __init__(self, stack: [], step_by_step=False):
        self.step_by_step = step_by_step
        super().__init__(stack)
        self.name = 'out_char'
        self.description = 'убирает значение из стэка ' \
                           'и выводит chr(значение) в консоль'

    def execute(self):
        if len(self.stack) == 0:
            return
        try:
            out_value = self.stack.pop()
            if self.step_by_step:
                print(f'\nВЫВОД:{chr(out_value)}\n')
            else:
                print(chr(out_value), end='')
            self.arguments = out_value
        except ValueError:
            return
