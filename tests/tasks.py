from microcelery import MicroCelery

app = MicroCelery()

@app.task
def func(x, y):
    print x + y

