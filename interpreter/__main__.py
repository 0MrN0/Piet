import argparse
import sys
from pathlib import Path

from interpreter.picture import Picture
from interpreter.piet_driver import PietDriver

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Piet Interpreter')
    parser.add_argument('script',
                        help='путь до программы-картинки',
                        type=str)
    parser.add_argument('-s', dest='step_by_step',
                        action='store_true',
                        help='выполнить в пошаговом режиме')
    args = parser.parse_args()
    script_path = Path(args.script)
    if not (script_path.exists() and script_path.is_file()):
        print('Файл не найден')
        exit(1)
    piet_driver = PietDriver(
        Picture.open_picture(script_path),
        args.step_by_step, sys.stdin, sys.stdout, sys.stderr)
    try:
        piet_driver.process_picture()
    except KeyboardInterrupt:
        print('Вы прервали обработку программы')
        exit(1)
