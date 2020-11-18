import argparse

from interpreter.picture import Picture
from interpreter.piet_driver import PietDriver

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Piet Interpreter')
    parser.add_argument('host',
                        help='name of picture format, which is in programs',
                        type=str)
    args = parser.parse_args()
    piet_driver = PietDriver(Picture.open_picture(args.host))
    piet_driver.process_picture()
