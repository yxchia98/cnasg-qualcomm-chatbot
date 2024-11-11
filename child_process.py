# child_process.py
from time import sleep

while True:
    # Make sure stdout writes are flushed to the stream
    print("Spam!", end=' ', flush=True)
    # Sleep to simulate some other work
    sleep(1)