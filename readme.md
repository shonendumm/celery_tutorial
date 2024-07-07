# Summary
Flask-Celery tutorial from https://medium.com/@Aman-tech/celery-with-flask-d1f1c555ceb7

A flask app that runs tasks using celery, by using redis or rabbitmq as the broker and result store.

The simulated long-running task here is to iterate up to the requested number of iterations, sleeping 2 seconds at every step.

# Overview
1. Start redis or rabbitmq server
2. Start celery worker
3. Start flask app
4. Send http requests to flask app, to start the tasks

## Prequisites:
1. install rabbitmq or redis
2. pip install -r requirements.txt

# Redis or RabbitMQ
To use redis or rabbitmq, this is set in the config.py file:

```
app.config.from_mapping(
    CELERY=dict(
        broker_url='amqp://myuser:123456@localhost:5672/myvhost',
        result_backend='rpc://',
        task_ignore_result=True,
    ),
)
```

# For redis
1. Start redis server at the cli
```
redis-server
```

2. Start the celery worker at the cli
```
celery -A tasks.celery_app worker --loglevel=info
```

3. Start the flask app in the project folder, cli
```
flask run
```

4. Send tasks to the flask server using curl or postman.
You can see the endpoint URLs in app.py file.
```
curl -X POST "http://localhost:5000/trigger_task?iterations=3"
```
This will return a json string with result_id:
```
{"result_id":"cd53c6f5-7d53-4dc5-895d-447c170b70c2"}
```

5. To get results, send a HTTP GET request with the result_id:
```
curl "http://localhost:5000/get_result?result_id=cd53c6f5-7d53-4dc5-895d-447c170b70c2"
```
This will return a json string with the task status and result:
```
{"ready":true,"successful":true,"value":45}
```


# For rabbitmq
Replace step 1 above by starting the rabbitmq server (instead of redis server) using 
```
rabbitmq-server
```
Then the rest of the steps are the same as for redis.

To stop the rabbitmq server, use:
```
rabbitmqctl stop
```
