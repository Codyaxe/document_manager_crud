import os
import platform

# def blinking_dots():
#     pass

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def flush_input():
    if platform.system() != 'Windows':
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    else:
        import msvcrt
        while msvcrt.kbhit():  
            msvcrt.getch()