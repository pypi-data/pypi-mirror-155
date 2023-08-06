''' Main of the package '''

# Import requirement

import tkinter as TK
import socket
import select
import sys
'''Replace "thread" with "_thread" for python 3'''
from atexit import register
import getpass
from logging.handlers import RotatingFileHandler
import os
import logging
from re import L
import sys
import traceback

from requests import patch

# Defining variables

def add_source_folder():
    os.system("mkdir src_folder")
    os.chdir("src_folder")
    os.system("mkdir example_folder")

import py

version = "0.0.1"

def about_python():
    print("Python version: ")
    print(py.__version__)
    print("Python Copyright")
    print("(c) Holger Krekel and others, 2004-2014")

def about_package():
    print("FoldToZip version :")
    print(version)

def chat():
    import time, socket, sys
    print('Setup Server...')
    time.sleep(1)
    #Get the hostname, IP Address from socket and set Port
    soc = socket.socket()
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    port = 1234
    soc.bind((host_name, port))
    print(host_name, '({})'.format(ip))
    name = input('Enter name: ')
    soc.listen(1) #Try to locate using socket
    print('Waiting for incoming connections...')
    connection, addr = soc.accept()
    print("Received connection from ", addr[0], "(", addr[1], ")\n")
    print('Connection Established. Connected From: {}, ({})'.format(addr[0], addr[0]))
    #get a connection from client side
    client_name = connection.recv(1024)
    client_name = client_name.decode()
    print(client_name + ' has connected.')
    print('Press [bye] to leave the chat room')
    connection.send(name.encode())
    while True:
        message = input('Me > ')
        if message == '[bye]':
            respondre = "Good Night..."
            connection.send(respondre.encode())
            print("\n")
            break
            connection.send(message.encode())
            message = connection.recv(1024)
            message = message.decode()
            print(client_name, '>', message)

def screen():
    screen = turtle.getscreen()

screen()