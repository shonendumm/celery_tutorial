from tasks import flask_app, long_running_task #-Line 1
from celery.result import AsyncResult #-Line 2 used to retrieve the result of a Celery task by its ID.
from flask import request, jsonify 

@flask_app.post("/trigger_task")
def start_task() -> dict[str, object]:
    iterations = request.args.get('iterations')
    print(iterations)
    # initiates the execution of the long_running_task Celery task asynchronously. 
    # The .delay() method schedules the task for execution and returns an instance of 
    # AsyncResult which represents the state and result of the task. 
    result = long_running_task.delay(int(iterations))#-Line 3
    return {"result_id": result.id}

@flask_app.get("/get_result")
def task_result() -> dict[str, object]:
    result_id = request.args.get('result_id')
    result = AsyncResult(result_id)#-Line 4
    if result.ready():#-Line 5
        # Task has completed
        if result.successful():#-Line 6
    
            return {
                "ready": result.ready(),
                "successful": result.successful(),
                "value": result.result,#-Line 7
            }
        else:
        # Task completed with an error
            return jsonify({'status': 'ERROR', 'error_message': str(result.result)})
    else:
        # Task is still pending
        return jsonify({'status': 'Running'})

if __name__ == "__main__":
    flask_app.run(debug=True)


# Run redis server using redis-server
# Run the Celery worker using celery -A tasks.celery_app worker --loglevel=info
# Run the Flask application using python app.py

# Trigger the task by sending a POST request to http://
# curl -X POST http://localhost:5000/trigger_task?iterations=10

# Retrieve the result of the task by sending a GET request to http://localhost:5000/get_result?result_id=<result_id>
# curl http://localhost:5000/get_result?result_id=<result_id>