# Piet_Interpreter
## Описание
Реализация интерпритатора языка Piet на питоне.

## Инструкция по установке
```bash 
git clone https://github.com/0MrN0/Piet.git
pip install -r requirements.txt
```

## Запуск
### Обычный режим исполнения
```bash
python -m interpreter picture_name
```
### Пошаговый режим исполнения
```bash
python -m interpreter -s picture_name
```

где picture_name - путь до программы.

## Тестовые программы
800-400.png выводит в консоль результат выражения 800 - 400

800-400_with_incorrect_color.png - аналог предыдущей программы,
но вместо белого цвета использует некоторый неизвестный языку цвет.

print_(.png выводит в консоль символ (

print_TLEN_use_switch.png выводит в консоль TLEN, в программе вручную изменяется cc

Comparsion_int.png ожидает от пользователя два числа на вход, после чего выводит
1, если первое число больше второго, 0, если они равны, в противном случае -1.
