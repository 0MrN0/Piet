import argparse
from pathlib import Path

from interpreter.picture import Picture
from interpreter.piet_driver import PietDriver

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Piet Interpreter')
    parser.add_argument('script',
                        help='name of picture format, which is in programs',
                        type=str, nargs='?')
    args = parser.parse_args()
    script_path = Path.cwd()/args.script
    if not script_path.exists():
        print('No such file')
        exit(1)
    piet_driver = PietDriver(Picture.open_picture(script_path))
    piet_driver.process_picture()
