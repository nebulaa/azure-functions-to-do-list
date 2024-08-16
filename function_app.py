import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

tasks = []

@app.route(route="add-task", methods=["POST"])
def add_task(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request to add a new task.')

    try:
        req_body = req.get_json()
        print("req_body", req_body)
        task_id = len(tasks) + 1
        task = {
            'id': task_id,
            'title': req_body.get('title')
        }
        tasks.append(task)
        return func.HttpResponse(json.dumps(task), status_code=201, mimetype="application/json")
    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

@app.route(route="get-task", methods=["GET"])
def get_task(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request to get task by id.')

    try:
        req_body = req.get_body()
        task_id = int(req.params["id"]) - 1
        return func.HttpResponse(json.dumps(tasks[task_id]), status_code=200, mimetype="application/json")
    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)
    
@app.route(route="update-task", methods=["PUT"])
def update_task(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request to update task by id.')

    try:
        task_id = int(req.params["id"]) - 1
        req_body = req.get_json()
        tasks[task_id]['title'] = req_body.get('title')
        return func.HttpResponse(json.dumps({"message": "Updated", "task": tasks[task_id]}), status_code=200, mimetype="application/json")
    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

@app.route(route="delete-task", methods=["DELETE"])
def delete_tasks(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request to delete task by id.')

    try:
        task_id = int(req.params["id"]) - 1
        tasks.pop(task_id)
        return func.HttpResponse("Deleted", status_code=200, mimetype="application/json")
    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)
    
@app.route(route="get-all-tasks", methods=["GET"])
def get_all_tasks(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request to get all tasks.')

    return func.HttpResponse(json.dumps(tasks), status_code=200, mimetype="application/json")