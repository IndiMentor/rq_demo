"""
This file contains the tasks that the huey task scheduler will execute based on the queue
"""
from time import sleep

def add(num):
    sleep(num)
    return num + num

def mult(num):
    return num * num
