from app import app
from app import r
from app import q
from app import tasks
from time import strftime

from flask import render_template, request

@app.route("/add-task", methods=["GET","POST"])
def add_task():
    jobs = q.jobs
    message = None
    url=None 
    
    if request.args:
        url = request.args.get("url")

        task = q.enqueue(tasks.count_words,url)

        jobs = q.jobs

        q_len = len(q)

        message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}.{q_len}"

    return render_template("add_task.html",message=message, jobs=jobs,url=url)