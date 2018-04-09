#!/usr/bin/python2

# Note that running python with the `-u` flag is required on Windows,
# in order to ensure that stdin and stdout are opened in binary, rather
# than text, mode.
from __future__ import print_function
import json
import sys
import atexit
import os
import struct

words = set()
fpath = '/tmp/webcomplete-fifo'

def makefifo(path):
    if not os.path.exists(path): 
        os.mkfifo(path)
    return open(path, 'w')
fifo = makefifo(fpath)

@atexit.register
def cleanup():
    global fifo
    global fpath
    if not fifo.closed:
        fifo.close()
    print("fifo closed", file=sys.stderr)

def update_file(words):
    global fifo
    if fifo.closed: return
    fifo.write('\r\n'.join(words))
    print("File updated", file=sys.stderr)

def update_words(newords):
    global words
    nws = set(newords)
    diff = nws - words
    words |= nws
    update_file(diff)

# Read a message from stdin and decode it.
def get_message():
    raw_length = sys.stdin.read(4)
    if not raw_length:
        sys.exit(0)
    message_length = struct.unpack('@I', raw_length)[0]
    message = sys.stdin.read(message_length)
    return json.loads(message)

# Encode a message for transmission, given its content.
def encode_message(message_content):
    encoded_content = json.dumps(message_content)
    encoded_length = struct.pack('@I', len(encoded_content))
    return {'length': encoded_length, 'content': encoded_content}


# Send an encoded message to stdout.
def send_message(encoded_message):
    sys.stdout.write(encoded_message['length'])
    sys.stdout.write(encoded_message['content'])
    sys.stdout.flush()

while True:
    message = get_message()
    if isinstance(message, list):
        update_words(message)
    #z send_message(encode_message(message))

