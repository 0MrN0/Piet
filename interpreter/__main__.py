import argparse
from pathlib import Path

from interpreter.picture import Picture
from interpreter.piet_driver import PietDriver

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Piet Interpreter')
    parser.add_argument('script',
                        help='name of picture format, which is in programs',
                        type=str)
    parser.add_argument('step_by_step',
                        help='1 - step_by_step, 0 - standard',
                        type=int)
    args = parser.parse_args()
    script_path = Path(args.script)
    if not (script_path.exists() and script_path.is_file()):
        print('No such file')
        exit(1)
    if not args.step_by_step:
        piet_driver = PietDriver(Picture.open_picture(script_path), False)
    else:
        piet_driver = PietDriver(Picture.open_picture(script_path), True)
    piet_driver.process_picture()
