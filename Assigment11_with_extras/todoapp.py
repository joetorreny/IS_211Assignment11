from flask import Flask, render_template, request, redirect
import re

priorities = {"High", "Medium", "Low"}


class ToDo:
    def __init__(self, task, email, priority):
        self.task = task
        self.email = email
        self.priority = priority


app = Flask(__name__)
todo_list = list()
current_error = ""
save_file = "save_file.txt"
# todo_list.append(ToDo("example1", "example1@yahoo.com", "High"))
# todo_list.append(ToDo("example2", "example2@yahoo.com", "Medium"))


@app.route('/')
def index():
    global current_error
    result = render_template("index.html", todo_list=todo_list, priorities=priorities, error=current_error)
    current_error = ""
    return result


@app.route('/submit', methods=["POST"])
def submit():
    task = request.form.get("task")
    email = request.form.get("email")
    priority = request.form.get("priority")
    priority_check = priority in priorities
    email_check = re.match("[^@]+@[^@]+\.[^@]+", email)
    if priority_check and email_check:
        todo = ToDo(task, email, priority)
        todo_list.append(todo)
    global current_error
    if not priority_check:
        current_error = "Wrong Priority"
    if not email_check:
        current_error += "Wrong Email"
    return redirect("/")


@app.route('/clear')
def clear():
    todo_list.clear()
    return redirect("/")


@app.route('/save')
def save():
    with open(save_file, "w+") as s_file:
        for todo in todo_list:
            s_file.write(todo.task + "\n")
            print(todo.task)
            s_file.write(todo.email + "\n")
            s_file.write(todo.priority + "\n")
    return redirect("/")


@app.route('/delete', methods=["POST"])
def delete():
    ind = int(request.form.get("delete"))
    del todo_list[ind]
    return redirect("/")


if __name__ == "__main__":
    lines = ""
    try:
        f = open(save_file, "r+")
        lines = f.readlines()
    except FileNotFoundError:
        pass
    first_ind = 0
    while first_ind < len(lines):
        cur_task = lines[first_ind].rstrip()
        cur_email = lines[first_ind + 1].rstrip()
        cur_priority = lines[first_ind + 2].rstrip()
        cur_todo = ToDo(cur_task, cur_email, cur_priority)
        todo_list.append(cur_todo)
        first_ind += 3

    app.run()
