#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import pandas as pd

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


df = pd.read_csv("last_24_hours2.csv")


for index, row in df.iterrows():
    date = row[0]
    cord1 = row[1]
    cord2 = row[2]
    id = row[3]

    #  Wait for next request from client
    message = socket.recv().decode()
    print(f"Received request: {message}")

    #  Do some 'work'
    time.sleep(0.01)

    #  Send reply back to client
    socket.send_string(f"{date} {cord1} {cord2} {id}")
