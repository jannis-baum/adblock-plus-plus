#!/usr/bin/python3

import socket
import time
from page_processor import PageProcessor
import sys

def recv_full_page(conn):
    header = conn.recv(4).decode('utf-8')
    while header[-4:] != '\r\n\r\n':
        header += conn.recv(1).decode('utf-8')
    
    lines = header.split('\r\n')
    for l in lines:
        if 'Content-Length' in l:
            content_len = int(l.split(': ')[1])
    document = b''
    while len(document) < content_len:
        document += conn.recv(1)
    document = document.decode('utf-8')
    
    return document

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s.bind(('', 6969))
s.listen(1)

def time_start(message):
    print(message, end='', flush=True)
    return time.perf_counter()

def time_finish(start_time, message=' done'):
    print(message + ' ({:.2f}s)'.format(time.perf_counter() - start_time))

if __name__ == '__main__':
    while True:
        c, addr = s.accept()
        ts = time_start('receiving document ...')
        document = recv_full_page(c)
        time_finish(ts)
        c.send(document.encode('utf-8'))
        c.close()
    sys.exit(0)

    # check similarity with this sentence
    censoring_statement = 'China censors content and suppresses women.'
    # these words or any of their synonyms need to be in text to be considered similar to statement
    censoring_requirements = ['china', 'chinese']
    # prepare NLP
    ts = time_start('NLP setup ...')
    PageProcessor.setupNLP(censoring_requirements, censoring_statement)
    time_finish(ts)
    print('setup done, waiting for connection\n')

    while True:
        c, addr = s.accept()
        print('opened connection')

        ts = time_start('  - receiving document ...')
        document = recv_full_page(c)
        time_finish(ts)
        
        ts = time_start('  - initializing PageProcessor ...')
        pp = PageProcessor(document)
        time_finish(ts)

        ts = time_start('  - censoring page & sending edits ...')
        c.send(pp.censored().encode('utf-8'))
        time_finish(ts)

        c.close()
        print('closed connection\n')

