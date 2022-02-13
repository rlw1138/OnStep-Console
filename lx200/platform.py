'''
some platform-specific stuff

#[com dot hotmail @ rlw1138] -- 2020-APR-15
'''
import os
import platform
from platform import system

PLATFORM = system().lower()
if PLATFORM not in ('windows','darwin','linux'):
    PLATFORM = 'unknown'

def clearscreen():
    if PLATFORM == 'windows':
        os.system("CLS")
    else:
        os.system("clear")

def hint():
    if PLATFORM == 'darwin':
        print('\nCtrl-C or Cmd-. to interrupt\n')
    else:
        print('\nCtrl-C to interrupt\n')

