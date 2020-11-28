from typing import List

from interpreter.directions import Direction, CodelChooser


class BaseCommand:
    name = 'no_action'
    description = 'эта команда ничего не делает'
    arguments = None

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: 'Direction', cc: 'CodelChooser'):
        pass

    def __repr__(self):
        return (f'\tназвание: {self.name},\n\tописание: '
                f'{self.description},\n\tаргументы: {self.arguments}')


class Push(BaseCommand):
    name = 'push'
    description = 'кладет в стэк число, равное количеству ' \
                  'пикселей в предыдущем блоке'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        self.arguments = len_current_block
        stack.append(self.arguments)


class Pop(BaseCommand):
    name = 'pop'
    description = 'убирает верхнее значение стэка'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        if len(stack) == 0:
            return
        self.arguments = stack.pop()


class Add(BaseCommand):
    name = 'add'
    description = 'убирает два значения из стэка, складывает их, ' \
                  'кладет результат обратно в стэк'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        if len(stack) < 2:
            return
        a = stack.pop()
        b = stack.pop()
        self.arguments = (a, b)
        stack.append(a + b)


class Subtract(BaseCommand):
    name = 'subtract'
    description = 'убирает два значения из стэка, вычитает верхнее из ' \
                  'предыдущего, кладет результат обратно в стэк'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        if len(stack) < 2:
            return
        a = stack.pop()
        b = stack.pop()
        self.arguments = (a, b)
        stack.append(b - a)


class Multiply(BaseCommand):
    name = 'multiply'
    description = 'Убирает два значения из стэка, умножает их, кладет ' \
                  'результат обратно в стэк'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        if len(stack) < 2:
            return
        a = stack.pop()
        b = stack.pop()
        self.arguments = (a, b)
        stack.append(a * b)


class Divide(BaseCommand):
    name = 'divide'
    description = 'убирает два значения из стэка, делит нацело предыдущее ' \
                  'на верхнее, кладет результат обратно в стэк'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        if len(stack) < 2:
            return
        a = stack.pop()
        b = stack.pop()
        self.arguments = (a, b)
        stack.append(b // a)


class Mod(BaseCommand):
    name = 'mod'
    description = 'убирает два значения из стэка, кладет остаток от ' \
                  'деления предыдущего на верхнее обратно в стэк'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        if len(stack) < 2:
            return
        a = stack.pop()
        b = stack.pop()
        self.arguments = (a, b)
        stack.append(b % abs(a))


class Not(BaseCommand):
    name = 'not'
    description = 'заменяет верхнее значение стэка на 0, если оно было ' \
                  'равно 1, иначе на 1'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        if len(stack) == 0:
            return
        old_value = stack.pop()
        self.arguments = old_value
        stack.append(1 if old_value == 0 else 0)


class Greater(BaseCommand):
    name = 'greater'
    description = 'убирает два значения из стэка, кладет в него 1, если ' \
                  'предыдущее значение было больше верхнего, иначе кладет 0'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        if len(stack) < 2:
            return
        a = stack.pop()
        b = stack.pop()
        self.arguments = (b, a)
        stack.append(1 if b > a else 0)


class Pointer(BaseCommand):
    name = 'pointer'
    description = 'убирает значение(далее х) из стэка, меняет dp по часовой' \
                  ' стрелке abs(x) раз, если х > 0, иначе - против часовой'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        new_dp = dp
        if len(stack) != 0:
            turn_count = stack.pop()
            self.arguments = turn_count
            for i in range(abs(turn_count)):
                new_dp = new_dp.next(turn_count > 0)
        return new_dp


class Switch(BaseCommand):
    name = 'switch'
    description = 'убирает значение(далее х) из стэка, меняет cc abs(x) раз'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        new_cc = cc
        if len(stack) != 0:
            turn_count = stack.pop()
            self.arguments = turn_count
            for i in range(abs(turn_count)):
                new_cc = new_cc.next()
        return new_cc


class Duplicate(BaseCommand):
    name = 'duplicate'
    description = 'дублирует в стэк его верхнее значение'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        if len(stack) == 0:
            return
        self.arguments = stack[-1]
        stack.append(stack[-1])


class Roll(BaseCommand):
    name = 'roll'
    description = 'убирает два значения из стэка, ' \
                  '\n\t\t  верхнее - count, предыдущее - depth, ' \
                  '\n\t\t  depth не может быть отрицательным, ' \
                  '\n\t\t  берет depth последних элементов стэка и ' \
                  '\n\t\t  циклически сдвигает их с шагом count ' \
                  '\n\t\t  (count > 0 - вправо, count < 0 - влево)'

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: Direction, cc: CodelChooser):
        if len(stack) < 2 or stack[-2] < 0:
            return
        count = stack.pop()
        depth = stack.pop()
        self.arguments = (depth, count)
        if depth == 1:
            return
        count %= depth
        index = -abs(count) + depth * (count < 0)
        stack[-depth:] = stack[index:] + stack[-depth:index]


class In(BaseCommand):
    def __init__(self, in_stream, error_stream):
        self.error_stream = error_stream
        self.in_stream = in_stream

    def _read_value(self) -> List[str]:
        chars = []
        while True:
            x = self.in_stream.read(1)
            if x == '\n' or not x:
                break
            chars.append(x)
        return chars


class InInt(In):
    name = 'in_int'
    description = 'кладет целое число, считанное с ' \
                  'указанного потока ввода в стэк'

    def __init__(self, in_stream, error_stream):
        super().__init__(in_stream, error_stream)

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: 'Direction', cc: 'CodelChooser'):
        chars = self._read_value()
        if len(chars) == 0:
            return
        number = 0
        k = 1
        sign = chars[0]
        if not sign.isdigit():
            if sign == '-':
                k = -1
            elif sign != '+':
                exit(1)
            chars = chars[1:]
        if len(chars) == 0:
            return
        for i in range(len(chars)):
            if not chars[i].isdigit():
                return
            number += int(chars[i]) * 10 ** (len(chars) - (i + 1)) * k
        self.arguments = number
        stack.append(number)


class InChar(In):
    name = 'in_char'
    description = 'кладет ord(считанный с указанного потока ввода) в стэк'

    def __init__(self, in_stream, error_stream):
        super().__init__(in_stream, error_stream)

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: 'Direction', cc: 'CodelChooser'):
        chars = self._read_value()
        try:
            if len(chars) > 1:
                return
            stack.append(ord(chars[0]))
            self.arguments = chars[0]
        except TypeError:
            return
        except ValueError:
            return


class Out(BaseCommand):
    def __init__(self, out_stream, error_stream):
        self.out_stream = out_stream
        self.error_stream = error_stream


class OutInt(Out):
    name = 'out_int'
    description = 'убирает значение из стэка и выводит ' \
                  'его в указанный поток вывода'

    def __init__(self, out_stream, error_stream):
        super().__init__(out_stream, error_stream)

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: 'Direction', cc: 'CodelChooser'):
        if len(stack) == 0:
            return
        out_value = stack.pop()
        self.arguments = out_value
        self.out_stream.write(str(out_value))


class OutChar(Out):
    name = 'out_char'
    description = 'убирает значение из стэка и выводит chr(значение) ' \
                  'в указанный поток вывода'

    def __init__(self, out_stream, error_stream):
        super().__init__(out_stream, error_stream)

    def __call__(self, stack: List[int], len_current_block: int,
                 dp: 'Direction', cc: 'CodelChooser'):
        if len(stack) == 0:
            return
        try:
            out_value = chr(stack.pop())
        except ValueError:
            return
        self.out_stream.write(out_value)
        self.arguments = out_value
