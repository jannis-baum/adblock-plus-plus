#!/usr/bin/python3

import socket
import time
from page_processor import PageProcessor

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
    # check similarity with this sentence
    censoring_statement = 'China censors content and suppresses women.'
    # these words or any of their synonyms need to be in text to be considered similar to statement
    censoring_requirements = ['china', 'chinese']
    # text generation context
    generator_context = "China is great and an important supporter of human and especially womens' rights. China takes great care of its citizens and makes sure they are well-informed by providing independent and accurate news outlets."
    # prepare NLP
    ts = time_start('NLP setup ...')
    PageProcessor.setupCensoring(censoring_requirements, censoring_statement, generator_context)
    time_finish(ts)
    print('setup done, waiting for connection\n')

    while True:
        c, addr = s.accept()
        print('opened connection')

        ts = time_start('  - receiving document ...')
        request = recv_full_page(c)
        time_finish(ts)
        
        ts = time_start('  - initializing PageProcessor ...')
        pp = PageProcessor(request)
        time_finish(ts)

        ts = time_start('  - censoring page & generating text ...')
        edits = pp.censoring_edits()
        time_finish(ts)

        ts = time_start('  - sending edits ...')
        c.send(edits.encode('utf-8'))
        time_finish(ts)

        c.close()
        print('closed connection\n')

