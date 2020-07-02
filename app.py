import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId  #inorder to use the id n match the id in mongo, we hv to convert to bson
from os import path 
if os.path.exists("env.py"):
     import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGODB_NAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())


@app.route("/add_task")
def add_task():
    return render_template("add-task.html",categories=mongo.db.categories.find())


@app.route("/insert_task",methods=["POST"])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for("get_tasks"))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    # fetching the task that matches this task ID.And we'll eventually redirect it to an edit task HTML
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edittask.html', task=the_task, categories=all_categories)


@app.route("/update_task/<task_id>",methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({"_id": ObjectId(task_id)},
      { 'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
          
      })
    return redirect(url_for("get_tasks"))

    
@app.route("/delete_task/<task_id>")
def delete_task(task_id):
    tasks  = mongo.db.tasks
    tasks.remove({"_id":ObjectId(task_id)})
    return redirect(url_for("get_tasks"))


@app.route("/get_categories")
def get_categories():
    return render_template("categories.html",categories=mongo.db.categories.find())


@app.route("/edit_category/<category_id>")
def edit_category(category_id):
    return render_template("editcategory.html", category= mongo.db.categories.find_one({"_id":ObjectId(category_id) }))


@app.route("/update_category/<category_id>",methods=["POST"])
def update_category(category_id):
    update_cat = mongo.db.categories.update(
        {"_id": ObjectId(category_id)},
        {"category_name": request.form.get("category_name")}
    )
    return redirect(url_for("get_categories"))


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id":ObjectId(category_id)})
    return redirect(url_for("get_categories"))


@app.route("/insert_category",methods=["POST"])
def insert_category():
    categories = mongo.db.categories
    doc_cat = {"category_name": request.form.get("category_name")}
    categories.insert_one(doc_cat)
    return redirect(url_for("get_categories"))


@app.route("/add_category")
def add_category():
    return render_template("addcategory.html")






if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)