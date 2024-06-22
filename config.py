# Tutorial from https://medium.com/@Aman-tech/celery-with-flask-d1f1c555ceb7

# Celery initialization with Flask


from celery import Celery, Task
from flask import Flask

def celery_init_app(app: Flask) -> Celery:
    # custom task that extends Celery's Task
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            # wrapper to ensure that tasks are run with app_context
            with app.app_context():
                return self.run(*args, **kwargs)

    # create celery instance
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    # set as default celery instance
    celery_app.set_default()
    # Store celery app in our app's extensions
    app.extensions["celery"] = celery_app
    return celery_app

# application factory pattern
def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
        ),
    )
    # app.config["CELERY"] = {
    #     "broker_url": "redis://localhost",
    #     "result_backend": "redis://localhost",
    #     "task_ignore_result": True,
    # }
    app.config.from_prefixed_env()
    celery_init_app(app)
    return app

