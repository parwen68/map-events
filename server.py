#!/usr/bin/env python
from flask import Flask, Response, render_template
app = Flask(__name__)

import multiprocessing
import sys
import time
import random
import datetime

queue = multiprocessing.JoinableQueue()
accessToken = None

def worker():
    while True:
        ts1 = datetime.datetime.now()
        time.sleep(10)
        num = random.randint(1,15)
        ts2 = datetime.datetime.now()
        diff = ts2 - ts1
        print diff.seconds
        for i in range(0, num):
            ts = random.uniform(0, diff.seconds)
            x = 55 + random.uniform(0,10)
            y = 10 + random.uniform(0,10)
            queue.put("%d %.5f %.5f" % (ts, x, y))

@app.route("/")
def index():
    return render_template("index.html", accessToken=accessToken)


@app.route("/subscribe")
def subscribe():
    print "subscribe"
    def gen():
        try:
            while True:
                result = queue.get()
                yield "data: %s\n\n" % result
        except GeneratorExit:
            pass        

    return Response(gen(), mimetype="text/event-stream")

if __name__ == "__main__":
    accessToken = sys.argv[1]
    p = multiprocessing.Process(target=worker)
    p.daemon = True
    p.start()
    app.run()