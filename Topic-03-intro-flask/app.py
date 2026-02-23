from flask import Flask, render_template, request, redirect, url_for

import sqlite3
from pprint import pprint
# remember to $ pip install flask
connection = sqlite3.connect("pets.db", check_same_thread=False)
print("succeeded in making connection.")
app = Flask(__name__)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
@app.route("/", methods=["GET"])
@app.route("/hello/<name>", methods=["GET"])
def get_hello(name="world"):
    # return f"<html><h1>Hello, {name}!<html>"
    return render_template("hello.html", name=name)
@app.route("/bye", methods=["GET"])
def get_bye():
    return "Bye!"
@app.route("/list", methods=["GET"])
def get_list():
    list = ["alpha","beta","gamma"]
    return render_template("list.html", list=list)
@app.route("/pets", methods=["GET"])
def get_pets():
    cursor = connection.execute("select * from pet")
    rows = cursor.fetchall()
    pprint(rows)
    return render_template("pets.html", pets=rows)
@app.route("/create", methods=["GET"])
def get_create():
    return render_template("create.html")

@app.route("/create", methods=["POST"])
def post_create():
    data = dict(request.form)
    cursor = connection.execute("""insert into pet(name, kind, age, food, weight) values (?,?,?,?,?)""",
        (data["name"],data["kind"],data["age"],data["food"], data["weight"]))
    rows = cursor.fetchall()
    connection.commit()
    return redirect(url_for("get_pets"))

@app.route("/update")
@app.route("/update/<id>", methods=["GET"])
def get_update(id):
    if id==None:
        return render_template("error.html", error_message="No ID was provided.")
    id = int(id)
    cursor = connection.cursor()
    cursor.execute("""select * from pet where id = ?""",(id,))
    rows = cursor.fetchall()
    print("DEBUG rows =", rows)

    try:
        (id, name, kind, age, food, weight) = rows[0]
        data = {
                "id":id,
                "name":name,
                "kind":kind,
                "age":age,
                "food":food,
                "weight": weight
        }
        print([data])
    except:
        return render_template("error.html", error_message="Data not found.")
    return render_template("update.html",data=data)

@app.route("/update")
@app.route("/update/<id>", methods=["POST"])
def post_update(id=None):
    if id==None:
        return render_template("error.html", error_message="No ID was provided.")
    id = int(id)
    data = dict(request.form)
    try:
        data["age"] = int(data["age"])
    except: 
        data["age"] = 0
    try:
        data["weight"] = float(data["weight"])
    except:
           data["weight"] = 0.0


    cursor = connection.cursor()
    cursor.execute("""update pet set name=?, kind=?, age=?, food=?, weight=? where id=?""",
        (data["name"],data["kind"],data["age"],data["food"], data["weight"], id))
    rows = cursor.fetchall()
    connection.commit()
    return redirect(url_for("get_pets"))

@app.route("/delete/<id>", methods=["GET"])
def get_delete(id):
    id = int(id)
    cursor = connection.execute("""delete from pet where id==?""",(id,))
    connection.commit()
    return redirect(url_for("get_pets"))