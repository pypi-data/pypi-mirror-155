#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Populate testapi with testscases - output messages.
"""

import sys

def print_skipped(msg = ''):
    """Print skipped message."""
    print(msg + '[\033[94mskipped\033[0m]')

def print_success(msg = ''):
    """Print success message."""
    print(msg + '[\033[92msuccess\033[0m]')

def print_failed_and_exit(msg):
    """Print failed message."""
    print('[\033[91mfailed\033[0m]')
    sys.exit(msg)

def print_job(msg):
    """Print job message."""
    print(msg, end=' ')
