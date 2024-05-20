from celery import Celery

app = Celery('tasks', backend='redis://clerk_redis:6379/0', broker='amqp://user:password@clerk_rabbitmq:5672//')

@app.task
def add(x, y):
    return x + y
