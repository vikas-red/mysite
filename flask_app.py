from flask import Flask, request, jsonify
from uuid import uuid4
from .mongodbClient import database


app = Flask(__name__)

# -----------------------------
# In-memory storage
# -----------------------------
todos = {}  # {id: todo_dict}


# -----------------------------
# Helpers
# -----------------------------
def get_todo_or_404(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        return None
    return todo


# -----------------------------
# Routes
# -----------------------------

@app.route("/", methods=["GET"])
def create_data():
    todoColl=database['todo']
    todoColl.insert_one({})
    return "My name is Vikas"


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    todo_id = str(uuid4())
    todo = {
        "id": todo_id,
        "title": data["title"],
        "description": data.get("description"),
        "completed": False
    }

    todos[todo_id] = todo
    return jsonify(todo), 201


@app.route("/todos", methods=["GET"])
def get_all_todos():
    return jsonify(list(todos.values())), 200


@app.route("/todos/<todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = get_todo_or_404(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo), 200


@app.route("/todos/<todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = get_todo_or_404(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    todo["title"] = data["title"]
    todo["description"] = data.get("description")
    return jsonify(todo), 200


@app.route("/todos/<todo_id>/complete", methods=["PATCH"])
def mark_complete(todo_id):
    todo = get_todo_or_404(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    todo["completed"] = True
    return jsonify(todo), 200


@app.route("/todos/<todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = get_todo_or_404(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    del todos[todo_id]
    return jsonify({"message": "Todo deleted successfully"}), 200
