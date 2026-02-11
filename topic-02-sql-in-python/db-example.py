import argparse
import sqlite3
from pprint import pprint
ap = argparse.ArgumentParser()
ap.add_argument("--db", default="pets.db")
args = ap.parse_args()
connection = sqlite3.connect(args.db)

print("Succeeded in making connection")

connection.execute("drop table if exists pet")
connection.commit()
print("dropped table pet (if it existed)")

connection.execute(
    """
create table pet(

id integer primary key autoincrement,
name text not null,
kind text not null,
age integer,
food text);
"""
)
connection.commit()
print("created table pet")

connection.execute("insert into pet (name, kind, age, food) values (?,?,?,?)", ("Daily", "Dog", 10, "catty"), 
)
connection.commit()
print("Inserted Daily")

connection.execute("insert into pet(name, kind, age, food) values (?,?,?,?)", ("Epson", "grey", 5, "Chicken"),)
connection.commit()
print("Inserted Epson")

connection.execute("insert into pet (name, kind, age, food) values (?,?,?,?)", ("Whiskey", "hamster", 4, "hamster cow"),)
connection.commit()
print("Inserted whiskers")

connection.execute("delete from pet where name=?",("Whiskey",))
connection.commit()
print("deleted whiskey")

connection.execute("update pet set age=? where name=?", (9, "Daily"))
connection.commit()
print("row updated")

print("try with a wrong name")
for i in [1,2]:
    try:
        connection.execute(
            "insert into petz(name, kind, age, food) values (?,?,?,?)",("Sandy", "cat", 6, "tuna"),
                           )
    except sqlite3.Error as e:
        print("caught sqlite error:", e)

print("try with the correct name")
for i in [1,2]:
    try:
        connection.execute(
            "insert into pet (name, kind, age, food) values (?,?,?,?)", ("Sandy", "cat", 7, "tuna"),
            
        )
        connection.commit()
        print("insert succeded")
        break
    except sqlite3.Error as e:
        print("caught sqlite error:", e)

cursor = connection.execute("select * from pet")
rows = cursor.fetchall()
print("rows in pet table:")
pprint(rows)

